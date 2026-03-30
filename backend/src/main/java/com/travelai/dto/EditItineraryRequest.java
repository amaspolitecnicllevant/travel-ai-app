package com.travelai.dto;

import jakarta.validation.constraints.NotBlank;

public record EditItineraryRequest(@NotBlank String prompt) {}
