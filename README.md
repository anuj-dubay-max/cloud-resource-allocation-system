# Cloud Resource Allocation System using Fuzzy Logic and Genetic Algorithms

An interactive Streamlit-based cloud resource allocation simulator that compares traditional Fuzzy Logic scheduling with a Hybrid Fuzzy Logic + Genetic Algorithm (GA) approach under server failure scenarios.

The system simulates cloud environments where user workloads compete for limited resources while maintaining load balance, resource utilization, and SLA compliance.

**Live Demo:** https://cloud-resource-allocation-system-h8byftneq86kkxmbty9nqf.streamlit.app/

---

## Overview

Cloud platforms must continuously allocate computing resources while handling fluctuating workloads, overloaded servers, and unexpected failures.

This project evaluates two different resource allocation strategies:

### Fuzzy Logic Allocation

A rule-based scheduler that evaluates server suitability using:

* User priority
* Resource demand
* Current server utilization

Allocation decisions are made greedily based on fuzzy scores.

### Hybrid Fuzzy + Genetic Algorithm Allocation

Uses the same fuzzy scoring system but incorporates a Genetic Algorithm to optimize resource allocation globally.

The GA searches for better user-to-server assignments by considering:

* Allocation success rate
* User satisfaction
* Load balancing
* SLA compliance
* Resource utilization

This allows the system to make more efficient allocation decisions under high-load and failure conditions.

---

## Key Features

* Interactive Streamlit Dashboard
* Cloud Resource Allocation Simulation
* Fuzzy Logic Based Scheduling
* Genetic Algorithm Optimization
* Server Failure Simulation
* Cascading Failure Modelling
* SLA Compliance Monitoring
* Load Balancing Analysis
* Real-Time Performance Metrics
* Comparative Visual Analytics

---

## System Architecture

```text
Users
(priority, CPU demand, memory demand, workload type)
        |
        v
Failure Simulation Layer
        |
        +----> Primary Server Failures
        |
        +----> Cascading Failures
        |
        +----> Recovery Events
        |
        v
+-------------------------------+
| Fuzzy Logic Allocation        |
| Rule-Based Greedy Scheduling  |
+-------------------------------+
        |
        v
Performance Metrics

+-------------------------------+
| Hybrid Allocation             |
| Fuzzy Logic + Genetic Algo    |
+-------------------------------+
        |
        v
Performance Metrics
```

---

## Workload Categories

The simulator generates different cloud workloads:

| Workload Type             | Distribution |
| ------------------------- | ------------ |
| Microservices             | 50%          |
| Web Applications          | 30%          |
| Batch Processing Jobs     | 15%          |
| Machine Learning Training | 5%           |

---

## SLA Management

Users with priority greater than or equal to 0.75 are classified as SLA-sensitive users.

The allocation engine applies additional resource safeguards to reduce the probability of rejection.

The system tracks:

* SLA violations
* High-priority request failures
* Allocation success rates
* User satisfaction scores

---

## Performance Metrics

The simulator compares both allocation approaches using:

* Allocation Success Rate
* User Satisfaction Score
* SLA Compliance Rate
* CPU Utilization
* Memory Utilization
* Load Balance Score
* High-Priority User Rejections

Example results under default settings:

| Metric               | Fuzzy Logic | Hybrid (Fuzzy + GA) |
| -------------------- | ----------- | ------------------- |
| Allocation Success   | ~72%        | ~89%                |
| SLA Compliance       | ~61%        | ~84%                |
| Load Balance Score   | ~0.71       | ~0.88               |
| Average Satisfaction | ~0.63       | ~0.74               |

---

## Dashboard Visualizations

The application provides:

* Resource Utilization Charts
* Server Health Monitoring
* GA Fitness Evolution Curves
* Workload Distribution Analysis
* SLA Compliance Statistics
* Performance Comparison Dashboard
* Server Heatmaps
* Allocation Success Reports

---

## Technology Stack

### Backend & Simulation

* Python
* NumPy
* Pandas

### Optimization

* Fuzzy Logic
* Genetic Algorithms

### Visualization

* Plotly

### User Interface

* Streamlit

---

## Run Locally

```bash
git clone https://github.com/YOUR_USERNAME/cloud-resource-allocation-system.git

cd cloud-resource-allocation-system

pip install -r requirements.txt

streamlit run resource_allocation_app.py
```

---

## Future Improvements

* Multi-Cloud Simulation
* Container Scheduling Support
* Kubernetes-inspired Orchestration
* Reinforcement Learning Based Scheduling
* Dynamic Auto-Scaling Policies
* Real-Time Monitoring Integration

---

## Author

Anuj Dubay

Computer Science Engineering
BMS College of Engineering, Bengaluru

GitHub: https://github.com/anuj-dubay-max
