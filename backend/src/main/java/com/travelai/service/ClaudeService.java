package com.travelai.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.LocalDate;

/**
 * Calls the Anthropic Claude API to generate or edit travel itineraries.
 * Falls back to a mock itinerary if ANTHROPIC_API_KEY is not configured.
 */
@Service
public class ClaudeService {

    @Value("${anthropic.api-key:}")
    private String apiKey;

    private static final String API_URL = "https://api.anthropic.com/v1/messages";
    private static final String MODEL = "claude-3-5-haiku-20241022";
    private final ObjectMapper objectMapper = new ObjectMapper();
    private final HttpClient httpClient = HttpClient.newHttpClient();

    public String generateItinerary(String destination, String type, LocalDate startDate, LocalDate endDate) {
        long days = java.time.temporal.ChronoUnit.DAYS.between(startDate, endDate) + 1;

        if (apiKey == null || apiKey.isBlank()) {
            return buildMockItinerary(destination, type, startDate, (int) days);
        }

        String prompt = String.format("""
            Generate a detailed %d-day travel itinerary for %s (type: %s) starting %s.

            Respond ONLY with valid JSON matching this exact structure:
            {
              "tripId": 0,
              "days": [
                {
                  "day": 1,
                  "date": "YYYY-MM-DD",
                  "activities": [
                    {
                      "time": "HH:MM",
                      "name": "Activity name",
                      "type": "cultural|gastronomy|leisure|tourist|transport",
                      "description": "Brief description",
                      "estimatedCost": 0
                    }
                  ]
                }
              ],
              "totalBudget": 0,
              "currency": "€"
            }

            Include 3-5 activities per day. Use realistic times, costs in euros.
            """, days, destination, type, startDate);

        return callClaude(prompt);
    }

    public String editItinerary(String currentItineraryJson, String userPrompt) {
        if (apiKey == null || apiKey.isBlank()) {
            return applyMockEdit(currentItineraryJson, userPrompt);
        }

        String prompt = String.format("""
            Edit the following travel itinerary based on this instruction: "%s"

            Current itinerary:
            %s

            Respond ONLY with the modified itinerary in the exact same JSON format.
            Keep the same structure, only modify the relevant parts.
            """, userPrompt, currentItineraryJson);

        return callClaude(prompt);
    }

    private String callClaude(String prompt) {
        try {
            String requestBody = objectMapper.writeValueAsString(new java.util.LinkedHashMap<>() {{
                put("model", MODEL);
                put("max_tokens", 4096);
                put("messages", java.util.List.of(
                    java.util.Map.of("role", "user", "content", prompt)
                ));
            }});

            HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(API_URL))
                .header("Content-Type", "application/json")
                .header("x-api-key", apiKey)
                .header("anthropic-version", "2023-06-01")
                .POST(HttpRequest.BodyPublishers.ofString(requestBody))
                .build();

            HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());

            JsonNode root = objectMapper.readTree(response.body());
            String text = root.path("content").get(0).path("text").asText();

            // Extract JSON from the response text
            int start = text.indexOf('{');
            int end = text.lastIndexOf('}') + 1;
            if (start >= 0 && end > start) {
                return text.substring(start, end);
            }
            return text;

        } catch (Exception e) {
            throw new RuntimeException("Error calling Claude API: " + e.getMessage(), e);
        }
    }

    private String buildMockItinerary(String destination, String type, LocalDate startDate, int days) {
        StringBuilder sb = new StringBuilder();
        sb.append(String.format("""
            {
              "tripId": 0,
              "days": [
            """));

        for (int i = 1; i <= days; i++) {
            LocalDate date = startDate.plusDays(i - 1);
            boolean last = (i == days);
            sb.append(String.format("""
                    {
                      "day": %d,
                      "date": "%s",
                      "activities": [
                        { "time": "09:00", "name": "Arrival & orientation in %s", "type": "tourist", "description": "Get to know the area", "estimatedCost": 0 },
                        { "time": "11:00", "name": "Main attraction visit", "type": "cultural", "description": "Explore the most iconic site", "estimatedCost": 15 },
                        { "time": "13:30", "name": "Local restaurant lunch", "type": "gastronomy", "description": "Try local cuisine", "estimatedCost": 20 },
                        { "time": "15:30", "name": "Afternoon leisure", "type": "leisure", "description": "Free time to explore", "estimatedCost": 10 },
                        { "time": "19:00", "name": "Dinner & local nightlife", "type": "gastronomy", "description": "Evening dinner", "estimatedCost": 30 }
                      ]
                    }%s
                """, i, date, destination, last ? "" : ","));
        }

        int totalBudget = days * 75;
        sb.append(String.format("""
              ],
              "totalBudget": %d,
              "currency": "€"
            }
            """, totalBudget));

        return sb.toString();
    }

    private String applyMockEdit(String currentJson, String prompt) {
        // Return current itinerary unchanged in mock mode, with a note
        return currentJson;
    }
}
