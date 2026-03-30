package com.travelai.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.util.Map;

/**
 * Calls the local Ollama instance to edit travel itineraries using a local LLM.
 */
@Service
public class OllamaService {

    @Value("${ollama.url:http://ollama:11434}")
    private String ollamaUrl;

    @Value("${ollama.model:llama3.2:1b}")
    private String model;

    private final ObjectMapper objectMapper = new ObjectMapper();
    private final HttpClient httpClient = HttpClient.newBuilder()
        .connectTimeout(Duration.ofSeconds(10))
        .build();

    public boolean isAvailable() {
        try {
            HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(ollamaUrl + "/api/tags"))
                .GET()
                .timeout(Duration.ofSeconds(5))
                .build();
            HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
            return response.statusCode() == 200;
        } catch (Exception e) {
            return false;
        }
    }

    public String editItinerary(String currentItineraryJson, String userPrompt) {
        String prompt = String.format("""
            You are a travel itinerary editor. Edit the following JSON itinerary based on the user instruction.

            User instruction: "%s"

            Current itinerary JSON:
            %s

            Rules:
            - Respond ONLY with valid JSON, no explanation, no markdown
            - Keep the exact same JSON structure
            - Only modify activities relevant to the instruction
            - Keep all day numbers and dates unchanged
            - estimatedCost must be a number (not a string)

            Modified itinerary JSON:
            """, userPrompt, currentItineraryJson);

        try {
            String requestBody = objectMapper.writeValueAsString(Map.of(
                "model", model,
                "prompt", prompt,
                "stream", false,
                "options", Map.of(
                    "temperature", 0.3,
                    "num_predict", 4096
                )
            ));

            HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(ollamaUrl + "/api/generate"))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(requestBody))
                .timeout(Duration.ofSeconds(120))
                .build();

            HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
            JsonNode root = objectMapper.readTree(response.body());
            String text = root.path("response").asText();

            // Extract JSON from response
            int start = text.indexOf('{');
            int end = text.lastIndexOf('}') + 1;
            if (start >= 0 && end > start) {
                String extracted = text.substring(start, end);
                // Validate it's parseable JSON
                objectMapper.readTree(extracted);
                return extracted;
            }

            // If no valid JSON found, return original
            return currentItineraryJson;

        } catch (Exception e) {
            // On any error, return original itinerary unchanged
            return currentItineraryJson;
        }
    }
}
