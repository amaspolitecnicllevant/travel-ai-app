package com.travelai.model;

import jakarta.persistence.*;

@Entity
@Table(name = "itineraries")
public class Itinerary {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(unique = true, nullable = false)
    private Long tripId;

    // Full itinerary stored as JSON text
    @Column(columnDefinition = "TEXT", nullable = false)
    private String content;

    public Itinerary() {}

    public Itinerary(Long tripId, String content) {
        this.tripId = tripId;
        this.content = content;
    }

    public Long getId() { return id; }
    public Long getTripId() { return tripId; }
    public String getContent() { return content; }

    public void setId(Long id) { this.id = id; }
    public void setTripId(Long tripId) { this.tripId = tripId; }
    public void setContent(String content) { this.content = content; }
}
