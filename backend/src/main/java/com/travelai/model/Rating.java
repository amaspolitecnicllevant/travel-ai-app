package com.travelai.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;

@Entity
@Table(name = "ratings")
public class Rating {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private Long tripId;

    @Column(nullable = false)
    private Long userId;

    @Min(1) @Max(5)
    @Column(nullable = false)
    private int score;

    private String comment;

    public Rating() {}

    public Long getId() { return id; }
    public Long getTripId() { return tripId; }
    public Long getUserId() { return userId; }
    public int getScore() { return score; }
    public String getComment() { return comment; }

    public void setId(Long id) { this.id = id; }
    public void setTripId(Long tripId) { this.tripId = tripId; }
    public void setUserId(Long userId) { this.userId = userId; }
    public void setScore(int score) { this.score = score; }
    public void setComment(String comment) { this.comment = comment; }
}
