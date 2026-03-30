package com.travelai.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import java.time.LocalDate;

public record TripRequest(
    @NotBlank String title,
    @NotBlank String destination,
    @NotBlank String type,
    @NotNull LocalDate startDate,
    @NotNull LocalDate endDate
) {}
