package com.travelai.controller;

import com.travelai.dto.RatingRequest;
import com.travelai.dto.RatingResponse;
import com.travelai.service.RatingService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/trips/{tripId}/ratings")
public class RatingController {

    private final RatingService ratingService;

    public RatingController(RatingService ratingService) {
        this.ratingService = ratingService;
    }

    @GetMapping
    public List<RatingResponse> getRatings(@PathVariable Long tripId) {
        return ratingService.getRatings(tripId);
    }

    @PostMapping
    public ResponseEntity<RatingResponse> addRating(@PathVariable Long tripId,
                                                     @Valid @RequestBody RatingRequest request,
                                                     @AuthenticationPrincipal UserDetails user) {
        RatingResponse rating = ratingService.addRating(tripId, request, user.getUsername());
        return ResponseEntity.status(HttpStatus.CREATED).body(rating);
    }
}
