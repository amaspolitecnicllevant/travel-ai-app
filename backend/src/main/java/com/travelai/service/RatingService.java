package com.travelai.service;

import com.travelai.dto.RatingRequest;
import com.travelai.dto.RatingResponse;
import com.travelai.model.Rating;
import com.travelai.repository.RatingRepository;
import com.travelai.repository.UserRepository;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class RatingService {

    private final RatingRepository ratingRepository;
    private final UserRepository userRepository;

    public RatingService(RatingRepository ratingRepository, UserRepository userRepository) {
        this.ratingRepository = ratingRepository;
        this.userRepository = userRepository;
    }

    public List<RatingResponse> getRatings(Long tripId) {
        return ratingRepository.findByTripId(tripId).stream()
            .map(RatingResponse::from)
            .toList();
    }

    public RatingResponse addRating(Long tripId, RatingRequest request, String email) {
        Long userId = userRepository.findByEmail(email)
            .orElseThrow(() -> new UsernameNotFoundException("User not found"))
            .getId();

        Rating rating = new Rating();
        rating.setTripId(tripId);
        rating.setUserId(userId);
        rating.setScore(request.score());
        rating.setComment(request.comment());
        ratingRepository.save(rating);

        return RatingResponse.from(rating);
    }
}
