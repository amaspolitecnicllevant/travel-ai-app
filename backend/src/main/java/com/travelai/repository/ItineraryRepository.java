package com.travelai.repository;

import com.travelai.model.Itinerary;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;

public interface ItineraryRepository extends JpaRepository<Itinerary, Long> {
    Optional<Itinerary> findByTripId(Long tripId);
}
