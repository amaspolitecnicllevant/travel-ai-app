package com.travelai.controller;

import com.travelai.dto.TripRequest;
import com.travelai.dto.TripResponse;
import com.travelai.service.TripService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/trips")
public class TripController {

    private final TripService tripService;

    public TripController(TripService tripService) {
        this.tripService = tripService;
    }

    @GetMapping
    public List<TripResponse> getTrips(@AuthenticationPrincipal UserDetails user) {
        return tripService.getTripsForUser(user.getUsername());
    }

    @GetMapping("/{id}")
    public TripResponse getTrip(@PathVariable Long id, @AuthenticationPrincipal UserDetails user) {
        return tripService.getTrip(id, user.getUsername());
    }

    @PostMapping
    public ResponseEntity<TripResponse> createTrip(@Valid @RequestBody TripRequest request,
                                                    @AuthenticationPrincipal UserDetails user) {
        TripResponse trip = tripService.createTrip(request, user.getUsername());
        return ResponseEntity.status(HttpStatus.CREATED).body(trip);
    }

    @PutMapping("/{id}")
    public TripResponse updateTrip(@PathVariable Long id,
                                   @Valid @RequestBody TripRequest request,
                                   @AuthenticationPrincipal UserDetails user) {
        return tripService.updateTrip(id, request, user.getUsername());
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteTrip(@PathVariable Long id,
                                           @AuthenticationPrincipal UserDetails user) {
        tripService.deleteTrip(id, user.getUsername());
        return ResponseEntity.noContent().build();
    }
}
