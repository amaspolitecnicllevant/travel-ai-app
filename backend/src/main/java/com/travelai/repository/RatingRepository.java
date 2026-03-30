package com.travelai.repository;

import com.travelai.model.Rating;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import java.util.List;
import java.util.Optional;

public interface RatingRepository extends JpaRepository<Rating, Long> {
    List<Rating> findByTripId(Long tripId);

    @Query("SELECT AVG(r.score) FROM Rating r WHERE r.tripId = :tripId")
    Optional<Double> findAverageScoreByTripId(Long tripId);
}
