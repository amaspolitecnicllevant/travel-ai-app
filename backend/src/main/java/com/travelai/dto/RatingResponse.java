package com.travelai.dto;

import com.travelai.model.Rating;

public record RatingResponse(Long id, Long tripId, Long userId, int score, String comment) {
    public static RatingResponse from(Rating r) {
        return new RatingResponse(r.getId(), r.getTripId(), r.getUserId(), r.getScore(), r.getComment());
    }
}
