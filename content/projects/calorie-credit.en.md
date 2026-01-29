+++
title = "Calorie Credit - Gamified Health Management Mini Program"
date = "2026-01-29T19:40:00+08:00"
draft = false
description = "A gamified health management WeChat Mini Program based on daily calorie credits."
tags = ["WeChat Mini Program", "uni-app", "AI", "Vue 3", "Health"]
categories = ["Project"]
+++

![Calorie Credit Interface](/images/projects/calorie-credit-main.png)

### Project Introduction

**Calorie Credit** is a health management WeChat Mini Program based on the concept of daily calorie limits.

The core philosophy is **gamification** of calorie management: helping users control their diet through the concept of "credit limits." Users have a certain calorie "credit limit" every day, and every meal is equivalent to "spending" credits, making healthy eating as intuitive and interesting as managing finances.

### Core Features

- **Daily Limit Management**: Automatically refreshes calorie credit at 0:00 daily. Visualizes remaining balance and provides alerts when the limit is low.
- **AI Food Recognition**: Integrated with **Zhipu AI GLM-4.6V**. Simply take a photo of your food to intelligently analyze the type and portion, automatically estimating calories.
- **Scientific Calculation**: Calculates Basal Metabolic Rate (BMR) based on the **Mifflin-St Jeor Equation**, combined with physical activity levels to determine Total Daily Energy Expenditure (TDEE).
- **Health Indicators**: Automatically calculates age and BMI based on user input, providing health status references.
- **Consumption Records**: Track every meal's calorie consumption like a ledger, with support for editing, deleting, and sharing.

### Tech Stack

- **Frontend Framework**: uni-app (Vue 3 + TypeScript)
- **UI Components**: uni-ui
- **State Management**: Pinia
- **Backend**: WeChat Cloud Development (Cloud Database, Cloud Functions, Cloud Storage)
- **AI Service**: Zhipu AI GLM-4.6V (Multimodal LLM)

### Scientific Basis

This project rigorously follows biological principles:
1.  **Mifflin-St Jeor Equation**: The internationally recognized standard for calculating BMR closest to modern human physiology.
2.  **TDEE Calculation**: Calculates real daily energy requirements based on physical activity levels.
3.  **Dynamic Age Adjustment**: Accounts for metabolic decline due to muscle loss, providing precise suggestions for users of different ages.

---

> By transforming the abstract concept of calories into intuitive "credit limits," Calorie Credit is dedicated to helping users easily establish healthy eating habits.
