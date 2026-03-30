package com.travelai.controller;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.travelai.dto.EditItineraryRequest;
import com.travelai.service.ItineraryService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/trips/{tripId}/itinerary")
public class ItineraryController {

    private final ItineraryService itineraryService;
    private final ObjectMapper objectMapper = new ObjectMapper();

    public ItineraryController(ItineraryService itineraryService) {
        this.itineraryService = itineraryService;
    }

    @GetMapping
    public ResponseEntity<JsonNode> getItinerary(@PathVariable Long tripId) throws Exception {
        String json = itineraryService.getItinerary(tripId);
        return ResponseEntity.ok(objectMapper.readTree(json));
    }

    @PostMapping
    public ResponseEntity<JsonNode> generateItinerary(@PathVariable Long tripId) throws Exception {
        String json = itineraryService.generateItinerary(tripId);
        return ResponseEntity.ok(objectMapper.readTree(json));
    }

    @PutMapping
    public ResponseEntity<JsonNode> editItinerary(@PathVariable Long tripId,
                                                   @Valid @RequestBody EditItineraryRequest request) throws Exception {
        String json = itineraryService.editItinerary(tripId, request.prompt());
        return ResponseEntity.ok(objectMapper.readTree(json));
    }
}
