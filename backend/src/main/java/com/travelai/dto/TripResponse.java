package com.travelai.dto;

import com.travelai.model.Trip;
import java.time.LocalDate;

public record TripResponse(
    Long id,
    String title,
    String destination,
    String type,
    LocalDate startDate,
    LocalDate endDate,
    Long userId,
    Double averageRating,
    String arrivalTime,
    String departureTime
) {
    public static TripResponse from(Trip trip, Double averageRating) {
        return new TripResponse(
            trip.getId(),
            trip.getTitle(),
            trip.getDestination(),
            trip.getType(),
            trip.getStartDate(),
            trip.getEndDate(),
            trip.getUserId(),
            averageRating,
            trip.getArrivalTime(),
            trip.getDepartureTime()
        );
    }
}
