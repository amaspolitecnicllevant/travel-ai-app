package com.travelai.service;

import com.travelai.dto.TripRequest;
import com.travelai.dto.TripResponse;
import com.travelai.model.Trip;
import com.travelai.repository.RatingRepository;
import com.travelai.repository.TripRepository;
import com.travelai.repository.UserRepository;
import org.springframework.http.HttpStatus;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;

@Service
public class TripService {

    private final TripRepository tripRepository;
    private final UserRepository userRepository;
    private final RatingRepository ratingRepository;

    public TripService(TripRepository tripRepository, UserRepository userRepository,
                       RatingRepository ratingRepository) {
        this.tripRepository = tripRepository;
        this.userRepository = userRepository;
        this.ratingRepository = ratingRepository;
    }

    public List<TripResponse> getTripsForUser(String email) {
        Long userId = getUserId(email);
        return tripRepository.findByUserId(userId).stream()
            .map(t -> TripResponse.from(t, getAvgRating(t.getId())))
            .toList();
    }

    public TripResponse getTrip(Long id, String email) {
        Trip trip = findTripOwnedBy(id, email);
        return TripResponse.from(trip, getAvgRating(id));
    }

    public TripResponse createTrip(TripRequest request, String email) {
        Long userId = getUserId(email);
        Trip trip = new Trip();
        trip.setTitle(request.title());
        trip.setDestination(request.destination());
        trip.setType(request.type());
        trip.setStartDate(request.startDate());
        trip.setEndDate(request.endDate());
        trip.setUserId(userId);
        tripRepository.save(trip);
        return TripResponse.from(trip, null);
    }

    public TripResponse updateTrip(Long id, TripRequest request, String email) {
        Trip trip = findTripOwnedBy(id, email);
        trip.setTitle(request.title());
        trip.setDestination(request.destination());
        trip.setType(request.type());
        trip.setStartDate(request.startDate());
        trip.setEndDate(request.endDate());
        tripRepository.save(trip);
        return TripResponse.from(trip, getAvgRating(id));
    }

    public void deleteTrip(Long id, String email) {
        findTripOwnedBy(id, email);
        tripRepository.deleteById(id);
    }

    public Trip getRawTrip(Long id) {
        return tripRepository.findById(id)
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Trip not found"));
    }

    private Trip findTripOwnedBy(Long id, String email) {
        Long userId = getUserId(email);
        Trip trip = tripRepository.findById(id)
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Trip not found"));
        if (!trip.getUserId().equals(userId)) {
            throw new ResponseStatusException(HttpStatus.FORBIDDEN, "Access denied");
        }
        return trip;
    }

    private Long getUserId(String email) {
        return userRepository.findByEmail(email)
            .orElseThrow(() -> new UsernameNotFoundException("User not found"))
            .getId();
    }

    private Double getAvgRating(Long tripId) {
        return ratingRepository.findAverageScoreByTripId(tripId).orElse(null);
    }
}
