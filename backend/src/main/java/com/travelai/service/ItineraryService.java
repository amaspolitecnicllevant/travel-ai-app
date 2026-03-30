package com.travelai.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.travelai.model.Itinerary;
import com.travelai.model.Trip;
import com.travelai.repository.ItineraryRepository;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

@Service
public class ItineraryService {

    private final ItineraryRepository itineraryRepository;
    private final TripService tripService;
    private final LocalDataService localDataService;
    private final ClaudeService claudeService;
    private final ObjectMapper objectMapper = new ObjectMapper();

    public ItineraryService(ItineraryRepository itineraryRepository, TripService tripService,
                            LocalDataService localDataService, ClaudeService claudeService) {
        this.itineraryRepository = itineraryRepository;
        this.tripService = tripService;
        this.localDataService = localDataService;
        this.claudeService = claudeService;
    }

    public String getItinerary(Long tripId) {
        Itinerary itinerary = itineraryRepository.findByTripId(tripId)
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "No hay itinerario para este viaje"));
        return withTripId(itinerary.getContent(), tripId);
    }

    public String generateItinerary(Long tripId) {
        Trip trip = tripService.getRawTrip(tripId);
        String json;

        // Use local DB for Costa del Sol destinations, Claude for others
        if (localDataService.supports(trip.getDestination())) {
            json = localDataService.generateItinerary(
                trip.getDestination(), trip.getType(),
                trip.getStartDate(), trip.getEndDate(),
                trip.getArrivalTime(), trip.getDepartureTime()
            );
        } else {
            json = claudeService.generateItinerary(
                trip.getDestination(), trip.getType(),
                trip.getStartDate(), trip.getEndDate()
            );
        }

        Itinerary itinerary = itineraryRepository.findByTripId(tripId)
            .orElse(new Itinerary(tripId, json));
        itinerary.setContent(json);
        itineraryRepository.save(itinerary);

        return withTripId(json, tripId);
    }

    public String editItinerary(Long tripId, String prompt) {
        Itinerary itinerary = itineraryRepository.findByTripId(tripId)
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND,
                "No hay itinerario. Genera uno primero."));

        String updatedJson = claudeService.editItinerary(itinerary.getContent(), prompt);
        itinerary.setContent(updatedJson);
        itineraryRepository.save(itinerary);

        return withTripId(updatedJson, tripId);
    }

    private String withTripId(String json, Long tripId) {
        try {
            ObjectNode node = (ObjectNode) objectMapper.readTree(json);
            node.put("tripId", tripId);
            return objectMapper.writeValueAsString(node);
        } catch (Exception e) {
            return json;
        }
    }
}
