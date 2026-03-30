package com.travelai.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Service;

import jakarta.annotation.PostConstruct;
import java.time.LocalDate;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.stream.StreamSupport;

/**
 * Generates itineraries from the local Costa del Sol database
 * (costa_del_sol.json) without calling any external API.
 */
@Service
public class LocalDataService {

    private final ObjectMapper mapper = new ObjectMapper();
    private List<JsonNode> allPlaces = new ArrayList<>();

    private static final Set<String> KNOWN_DESTINATIONS = Set.of(
        "málaga", "malaga",
        "benalmádena", "benalmadena",
        "marbella",
        "torremolinos",
        "fuengirola",
        "nerja",
        "ronda"
    );

    @PostConstruct
    public void loadData() {
        try {
            JsonNode root = mapper.readTree(new ClassPathResource("costa_del_sol.json").getInputStream());
            root.path("places").forEach(allPlaces::add);
        } catch (Exception e) {
            throw new RuntimeException("Failed to load costa_del_sol.json", e);
        }
    }

    public boolean supports(String destination) {
        return KNOWN_DESTINATIONS.contains(destination.toLowerCase().trim());
    }

    public String generateItinerary(String destination, String tripType,
                                    LocalDate startDate, LocalDate endDate,
                                    String arrivalTime, String departureTime) {

        List<JsonNode> places = filterByDestination(destination);
        int days = (int) (java.time.temporal.ChronoUnit.DAYS.between(startDate, endDate) + 1);

        // Separate by type
        List<JsonNode> monuments  = filterByType(places, "monument");
        List<JsonNode> freeTours  = filterByType(places, "freetour");
        List<JsonNode> activities = filterByType(places, "activity");
        List<JsonNode> restaurants = filterByType(places, "restaurant");

        // Sort by trip type affinity
        Comparator<JsonNode> relevance = tripTypeComparator(tripType);
        monuments.sort(relevance);
        freeTours.sort(relevance);
        activities.sort(relevance);
        restaurants.sort(relevance);

        Set<String> used = new HashSet<>();
        ArrayNode daysArray = mapper.createArrayNode();
        double totalBudget = 0;

        for (int d = 1; d <= days; d++) {
            LocalDate date = startDate.plusDays(d - 1);
            String dayStart = (d == 1 && arrivalTime != null && !arrivalTime.isBlank())
                ? arrivalTime : "09:00";
            String dayEnd   = (d == days && departureTime != null && !departureTime.isBlank())
                ? departureTime : "22:00";

            ObjectNode dayNode = mapper.createObjectNode();
            dayNode.put("day", d);
            dayNode.put("date", date.toString());
            ArrayNode activitiesArray = mapper.createArrayNode();

            LocalTime current = parseTime(dayStart);
            LocalTime end     = parseTime(dayEnd);

            // Morning slot: free tour or monument
            if (current.isBefore(LocalTime.of(13, 0))) {
                JsonNode place = pickOne(freeTours, used);
                if (place == null) place = pickOne(monuments, used);
                if (place != null) {
                    activitiesArray.add(toActivity(place, timeStr(current)));
                    markUsed(used, place);
                    current = current.plusMinutes(place.path("durationMinutes").asInt(90) + 30);
                    totalBudget += place.path("estimatedCost").asDouble(0);
                }
            }

            // Lunch restaurant
            LocalTime lunchTime = LocalTime.of(13, 30);
            if (!current.isAfter(lunchTime) && end.isAfter(LocalTime.of(14, 0))) {
                JsonNode restaurant = pickOne(restaurants, used);
                if (restaurant != null) {
                    activitiesArray.add(toActivity(restaurant, timeStr(lunchTime)));
                    markUsed(used, restaurant);
                    current = lunchTime.plusMinutes(restaurant.path("durationMinutes").asInt(90));
                    totalBudget += restaurant.path("estimatedCost").asDouble(0);
                }
            }

            // Afternoon slot: activity or monument
            if (current.isBefore(LocalTime.of(18, 0)) && end.isAfter(LocalTime.of(16, 0))) {
                JsonNode place = pickOne(activities, used);
                if (place == null) place = pickOne(monuments, used);
                if (place != null) {
                    LocalTime slotTime = current.isBefore(LocalTime.of(15, 30))
                        ? LocalTime.of(15, 30) : current;
                    activitiesArray.add(toActivity(place, timeStr(slotTime)));
                    markUsed(used, place);
                    current = slotTime.plusMinutes(place.path("durationMinutes").asInt(60) + 15);
                    totalBudget += place.path("estimatedCost").asDouble(0);
                }
            }

            // Dinner restaurant (only if time allows)
            if (end.isAfter(LocalTime.of(20, 0))) {
                JsonNode restaurant = pickOne(restaurants, used);
                if (restaurant != null) {
                    activitiesArray.add(toActivity(restaurant, "20:00"));
                    markUsed(used, restaurant);
                    totalBudget += restaurant.path("estimatedCost").asDouble(0);
                }
            }

            dayNode.set("activities", activitiesArray);
            daysArray.add(dayNode);
        }

        ObjectNode result = mapper.createObjectNode();
        result.put("tripId", 0);
        result.set("days", daysArray);
        result.put("totalBudget", Math.round(totalBudget));
        result.put("currency", "€");
        result.put("source", "local-database");

        try {
            return mapper.writeValueAsString(result);
        } catch (Exception e) {
            throw new RuntimeException("Error serializing itinerary", e);
        }
    }

    // ---- helpers ----

    private List<JsonNode> filterByDestination(String destination) {
        String dest = destination.toLowerCase().trim();
        return allPlaces.stream()
            .filter(p -> p.path("destination").asText("").toLowerCase().contains(dest)
                || dest.contains(p.path("destination").asText("").toLowerCase()))
            .collect(java.util.stream.Collectors.toList());
    }

    private List<JsonNode> filterByType(List<JsonNode> places, String type) {
        return places.stream()
            .filter(p -> type.equals(p.path("type").asText("")))
            .collect(java.util.stream.Collectors.toCollection(ArrayList::new));
    }

    private Comparator<JsonNode> tripTypeComparator(String tripType) {
        return (a, b) -> {
            int scoreA = tagScore(a, tripType);
            int scoreB = tagScore(b, tripType);
            if (scoreA != scoreB) return scoreB - scoreA;
            return Double.compare(
                b.path("rating").asDouble(0),
                a.path("rating").asDouble(0)
            );
        };
    }

    private int tagScore(JsonNode place, String tripType) {
        String tags = place.path("tags").toString().toLowerCase();
        return switch (tripType.toLowerCase()) {
            case "familiar"   -> (tags.contains("familiar")  ? 2 : 0);
            case "romantico"  -> (tags.contains("romantico") ? 2 : 0);
            case "aventura"   -> (tags.contains("aventura")  ? 2 : 0);
            case "mochilero"  -> (tags.contains("mochilero") ? 2 : 0) +
                                 (place.path("estimatedCost").asDouble(1) == 0 ? 1 : 0);
            case "cultural"   -> (tags.contains("cultural")  ? 2 : 0) +
                                 (tags.contains("historia")   ? 1 : 0);
            default           -> 0;
        };
    }

    private final Map<String, Integer> cycleIndex = new ConcurrentHashMap<>();

    private JsonNode pickOne(List<JsonNode> list, Set<String> used) {
        if (list.isEmpty()) return null;
        // First try unused places
        JsonNode unused = list.stream()
            .filter(p -> !used.contains(p.path("id").asText()))
            .findFirst()
            .orElse(null);
        if (unused != null) return unused;
        // All used: cycle through list with round-robin to avoid repeating same item
        String key = list.get(0).path("destination").asText() + list.get(0).path("type").asText();
        int idx = cycleIndex.getOrDefault(key, 0) % list.size();
        cycleIndex.put(key, idx + 1);
        return list.get(idx);
    }

    private void markUsed(Set<String> used, JsonNode place) {
        used.add(place.path("id").asText());
    }

    private ObjectNode toActivity(JsonNode place, String time) {
        ObjectNode act = mapper.createObjectNode();
        act.put("time", time);
        act.put("name", place.path("name").asText());
        act.put("type", place.path("type").asText());
        act.put("description", place.path("description").asText());
        act.put("estimatedCost", place.path("estimatedCost").asDouble(0));
        act.put("address", place.path("address").asText());
        act.put("openingHours", place.path("openingHours").asText());
        act.put("rating", place.path("rating").asDouble(0));
        return act;
    }

    private LocalTime parseTime(String time) {
        try {
            return LocalTime.parse(time, DateTimeFormatter.ofPattern("HH:mm"));
        } catch (Exception e) {
            return LocalTime.of(9, 0);
        }
    }

    private String timeStr(LocalTime time) {
        return time.format(DateTimeFormatter.ofPattern("HH:mm"));
    }
}
