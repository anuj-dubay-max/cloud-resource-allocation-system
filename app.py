"""
Fuzzy Logic vs Hybrid (Fuzzy+GA) Resource Allocation System
============================================================
Streamlit Dashboard — Resume-grade demo
"""

import streamlit as st
import random
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional
import time
import warnings

warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Resource Allocation: Fuzzy vs Hybrid",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS — Dark industrial tech aesthetic
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* Global */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #0a0e1a;
    color: #e2e8f0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0f1629 !important;
    border-right: 1px solid #1e2d4a;
}

[data-testid="stSidebar"] .stMarkdown p {
    color: #94a3b8;
    font-size: 0.82rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

/* Header */
.main-header {
    background: linear-gradient(135deg, #0f1629 0%, #1a2744 50%, #0f1629 100%);
    border: 1px solid #1e3a5f;
    border-radius: 12px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}

.main-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(56,189,248,0.07) 0%, transparent 70%);
    pointer-events: none;
}

.main-header h1 {
    font-family: 'Space Mono', monospace;
    font-size: 1.6rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0 0 0.3rem 0;
    letter-spacing: -0.02em;
}

.main-header p {
    color: #64748b;
    font-size: 0.92rem;
    margin: 0;
}

.tag {
    display: inline-block;
    background: rgba(56,189,248,0.1);
    border: 1px solid rgba(56,189,248,0.3);
    color: #38bdf8;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    padding: 2px 8px;
    border-radius: 4px;
    margin-right: 6px;
    margin-top: 8px;
}

/* Metric cards */
.metric-card {
    background: #0f1629;
    border: 1px solid #1e2d4a;
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
}

.metric-card:hover {
    border-color: #38bdf8;
}

.metric-card .label {
    font-size: 0.72rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-family: 'Space Mono', monospace;
    margin-bottom: 0.4rem;
}

.metric-card .value {
    font-family: 'Space Mono', monospace;
    font-size: 1.8rem;
    font-weight: 700;
    line-height: 1;
}

.metric-card .delta {
    font-size: 0.75rem;
    margin-top: 0.3rem;
    font-family: 'Space Mono', monospace;
}

.val-green { color: #34d399; }
.val-red   { color: #f87171; }
.val-blue  { color: #38bdf8; }
.val-amber { color: #fbbf24; }

/* Section headers */
.section-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: #38bdf8;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    margin-bottom: 0.8rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid #1e2d4a;
}

/* Status badges */
.badge-fuzzy {
    background: rgba(248,113,113,0.15);
    border: 1px solid rgba(248,113,113,0.4);
    color: #f87171;
    padding: 3px 10px;
    border-radius: 20px;
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    font-weight: 700;
}

.badge-hybrid {
    background: rgba(52,211,153,0.15);
    border: 1px solid rgba(52,211,153,0.4);
    color: #34d399;
    padding: 3px 10px;
    border-radius: 20px;
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    font-weight: 700;
}

/* Divider */
.divider {
    border: none;
    border-top: 1px solid #1e2d4a;
    margin: 1.5rem 0;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #0369a1, #0284c7);
    color: white;
    border: none;
    border-radius: 8px;
    font-family: 'Space Mono', monospace;
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    padding: 0.6rem 1.8rem;
    transition: all 0.2s;
    width: 100%;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #0284c7, #38bdf8);
    box-shadow: 0 0 20px rgba(56,189,248,0.3);
    transform: translateY(-1px);
}

/* Sliders */
.stSlider > div > div > div {
    background: #38bdf8 !important;
}

/* Progress */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #0369a1, #38bdf8) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #0f1629;
    border-bottom: 1px solid #1e2d4a;
    gap: 4px;
}

.stTabs [data-baseweb="tab"] {
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    color: #64748b !important;
    border-radius: 6px 6px 0 0;
    padding: 8px 20px;
}

.stTabs [aria-selected="true"] {
    color: #38bdf8 !important;
    border-bottom: 2px solid #38bdf8;
    background: rgba(56,189,248,0.05) !important;
}

/* Expander */
.streamlit-expanderHeader {
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    color: #94a3b8;
    background: #0f1629;
    border: 1px solid #1e2d4a;
    border-radius: 8px;
}

/* plotly chart backgrounds */
.js-plotly-plot .plotly .bg {
    fill: transparent !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# CORE MODELS (same logic, same seed)
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class Config:
    RANDOM_SEED: int = 42
    NUM_SERVERS: int = 12
    SERVER_CPU_OPTIONS: list = field(default_factory=lambda: [4, 8, 16, 32])
    MEMORY_TO_CPU_RATIO: float = 4.0
    NUM_USERS: int = 300
    FAILURE_PROBABILITY: float = 0.30
    CASCADING_FAILURE_PROB: float = 0.20
    RECOVERY_RATE: float = 0.40
    SLA_HIGH_PRIORITY_THRESHOLD: float = 0.75
    SLA_GUARANTEE_FACTOR: float = 0.60
    GA_POPULATION_SIZE: int = 60
    GA_GENERATIONS: int = 40
    GA_CROSSOVER_RATE: float = 0.85
    GA_MUTATION_RATE: float = 0.12
    GA_ELITE_SIZE: int = 4
    GA_TOURNAMENT_SIZE: int = 5
    FUZZY_RULE_COUNT: int = 27
    WORKLOAD_MIX: dict = field(default_factory=lambda: {
        'microservices': 0.50,
        'web_apps': 0.30,
        'batch_jobs': 0.15,
        'ml_training': 0.05
    })


@dataclass
class User:
    id: int
    priority: float
    cpu_demand: float
    mem_demand: float
    workload_type: str
    arrival_time: float = 0.0
    sla_sensitive: bool = False

    def __post_init__(self):
        self.sla_sensitive = self.priority >= 0.75


@dataclass
class Server:
    id: int
    cpu_capacity: float
    mem_capacity: float
    is_online: bool = True
    current_cpu_load: float = 0.0
    current_mem_load: float = 0.0
    failure_count: int = 0

    def available_cpu(self) -> float:
        return max(0.0, self.cpu_capacity - self.current_cpu_load) if self.is_online else 0.0

    def available_mem(self) -> float:
        return max(0.0, self.mem_capacity - self.current_mem_load) if self.is_online else 0.0

    def utilization(self) -> float:
        if not self.is_online or self.cpu_capacity == 0:
            return 0.0
        return min(1.0, self.current_cpu_load / self.cpu_capacity)

    def memory_utilization(self) -> float:
        if not self.is_online or self.mem_capacity == 0:
            return 0.0
        return min(1.0, self.current_mem_load / self.mem_capacity)

    def can_accommodate(self, user: 'User', safety_margin: float = 0.0) -> bool:
        if not self.is_online:
            return False
        return (self.available_cpu() >= user.cpu_demand * (1 + safety_margin) and
                self.available_mem() >= user.mem_demand * (1 + safety_margin))


@dataclass
class AllocationResult:
    allocated: List[Dict] = field(default_factory=list)
    rejected: List[int] = field(default_factory=list)
    servers: List[Server] = field(default_factory=list)
    high_priority_violations: int = 0
    total_satisfaction: float = 0.0


# ─────────────────────────────────────────────────────────────────────────────
# FUZZY CONTROLLER
# ─────────────────────────────────────────────────────────────────────────────

class FuzzyLogicController:
    def __init__(self, cfg: Config, rule_weights=None):
        if rule_weights is None:
            rng = np.random.RandomState(cfg.RANDOM_SEED)
            self.rule_weights = rng.uniform(0.5, 1.0, cfg.FUZZY_RULE_COUNT)
        else:
            self.rule_weights = np.clip(rule_weights, 0.1, 1.0)

    def fuzzify(self, x: float) -> Dict[str, float]:
        x = float(np.clip(x, 0.0, 1.0))
        low = max(0.0, min(1.0, (0.7 - x) / 0.7))
        high = max(0.0, min(1.0, (x - 0.3) / 0.7))
        medium = max(0.0, 1.0 - abs(x - 0.5) * 2.0)
        return {"low": low, "medium": medium, "high": high}

    def evaluate_rules(self, pf, df, lf) -> float:
        levels = ['low', 'medium', 'high']
        ws, ts = 0.0, 0.0
        ri = 0
        for p in levels:
            for d in levels:
                for l in levels:
                    s = min(pf[p], df[d], lf[l])
                    if s > 0:
                        ws += s * self.rule_weights[ri]
                        ts += s
                    ri += 1
        return ws / max(ts, 1e-9)

    def score(self, user: User, server: Server) -> float:
        pf = self.fuzzify(user.priority)
        dn = np.clip(user.cpu_demand / max(server.cpu_capacity * 0.8, 1e-6), 0, 1)
        df = self.fuzzify(dn)
        lf = self.fuzzify(1.0 - server.utilization())
        base = self.evaluate_rules(pf, df, lf)
        if user.sla_sensitive:
            base *= 1.25
        return float(np.clip(base, 0, 1))


# ─────────────────────────────────────────────────────────────────────────────
# INFRASTRUCTURE
# ─────────────────────────────────────────────────────────────────────────────

def init_servers(cfg: Config) -> List[Server]:
    rng = np.random.RandomState(cfg.RANDOM_SEED)
    servers = []
    for i in range(cfg.NUM_SERVERS):
        cpu = float(rng.choice(cfg.SERVER_CPU_OPTIONS))
        mem = cpu * cfg.MEMORY_TO_CPU_RATIO
        servers.append(Server(id=i, cpu_capacity=cpu, mem_capacity=mem,
                               current_cpu_load=cpu * rng.uniform(0.15, 0.35),
                               current_mem_load=mem * rng.uniform(0.15, 0.35)))
    return servers


def simulate_failures(servers: List[Server], cfg: Config) -> Dict:
    rng = np.random.RandomState(cfg.RANDOM_SEED + 1)
    failed, cascade = [], []
    for s in servers:
        if s.is_online and rng.rand() < cfg.FAILURE_PROBABILITY:
            s.is_online = False
            s.current_cpu_load = 0.0
            s.current_mem_load = 0.0
            s.failure_count += 1
            failed.append(s.id)
    if failed:
        online = [s for s in servers if s.is_online]
        for s in online:
            if s.utilization() > rng.uniform(0.70, 0.95):
                if rng.rand() < cfg.CASCADING_FAILURE_PROB:
                    s.is_online = False
                    s.current_cpu_load = 0.0
                    s.current_mem_load = 0.0
                    s.failure_count += 1
                    cascade.append(s.id)
    return {'primary': failed, 'cascade': cascade, 'total': len(failed) + len(cascade)}


def gen_users(cfg: Config) -> List[User]:
    rng = np.random.RandomState(cfg.RANDOM_SEED)
    workload_types = list(cfg.WORKLOAD_MIX.keys())
    workload_probs = list(cfg.WORKLOAD_MIX.values())
    users = []
    for i in range(cfg.NUM_USERS):
        wt = rng.choice(workload_types, p=workload_probs)
        pri = float(np.clip(rng.beta(2.5, 3.0), 0, 1))
        if wt == 'microservices':
            cpu, mem = rng.uniform(0.25, 2.0), rng.uniform(0.5, 4.0)
        elif wt == 'web_apps':
            cpu, mem = rng.uniform(1.5, 6.0), rng.uniform(4.0, 16.0)
        elif wt == 'batch_jobs':
            cpu, mem = rng.uniform(4.0, 12.0), rng.uniform(8.0, 48.0)
        else:
            cpu, mem = rng.uniform(8.0, 24.0), rng.uniform(32.0, 128.0)
        users.append(User(id=i, priority=pri,
                          cpu_demand=cpu * rng.uniform(0.8, 1.3),
                          mem_demand=mem * rng.uniform(0.8, 1.3),
                          workload_type=wt,
                          arrival_time=float(i * 0.5)))
    return users


# ─────────────────────────────────────────────────────────────────────────────
# FUZZY-ONLY ALLOCATION
# ─────────────────────────────────────────────────────────────────────────────

def fuzzy_only_allocation(users: List[User], servers: List[Server], fz: FuzzyLogicController, cfg: Config) -> AllocationResult:
    result = AllocationResult(servers=[Server(s.id, s.cpu_capacity, s.mem_capacity, s.is_online,
                                               s.current_cpu_load, s.current_mem_load) for s in servers])
    sim_servers = result.servers
    sorted_users = sorted(enumerate(users), key=lambda x: -x[1].priority)

    for ui, user in sorted_users:
        best, best_score = None, -1.0
        safety = cfg.SLA_GUARANTEE_FACTOR if user.sla_sensitive else 0.0
        for sv in sim_servers:
            if sv.can_accommodate(user, safety):
                sc = fz.score(user, sv)
                if sc > best_score:
                    best_score, best = sc, sv
        if best:
            best.current_cpu_load += user.cpu_demand
            best.current_mem_load += user.mem_demand
            sat = fz.score(user, best)
            result.allocated.append({'user_id': user.id, 'server_id': best.id,
                                      'satisfaction': sat, 'priority': user.priority,
                                      'workload_type': user.workload_type})
            result.total_satisfaction += sat
        else:
            result.rejected.append(user.id)
            if user.sla_sensitive:
                result.high_priority_violations += 1
    return result


# ─────────────────────────────────────────────────────────────────────────────
# GENETIC ALGORITHM
# ─────────────────────────────────────────────────────────────────────────────

class GeneticAlgorithm:
    def __init__(self, users, servers, fz, cfg: Config):
        self.users = users
        self.servers = servers
        self.fz = fz
        self.cfg = cfg
        self.n_users = len(users)
        self.n_servers = len(servers)
        self.best_history = []
        self.avg_history = []

    def _sim(self, chrom: np.ndarray) -> AllocationResult:
        sim_sv = [Server(s.id, s.cpu_capacity, s.mem_capacity, s.is_online,
                          s.current_cpu_load, s.current_mem_load) for s in self.servers]
        result = AllocationResult(servers=sim_sv)
        for user in sorted(self.users, key=lambda u: u.arrival_time):
            sid = int(chrom[user.id])
            if sid < 0 or sid >= len(sim_sv):
                result.rejected.append(user.id)
                if user.sla_sensitive: result.high_priority_violations += 1
                continue
            sv = sim_sv[sid]
            safety = self.cfg.SLA_GUARANTEE_FACTOR if user.sla_sensitive else 0.0
            if sv.can_accommodate(user, safety):
                sv.current_cpu_load += user.cpu_demand
                sv.current_mem_load += user.mem_demand
                sat = self.fz.score(user, sv)
                result.allocated.append({'user_id': user.id, 'server_id': sv.id,
                                          'satisfaction': sat, 'priority': user.priority,
                                          'workload_type': user.workload_type})
                result.total_satisfaction += sat
            else:
                result.rejected.append(user.id)
                if user.sla_sensitive: result.high_priority_violations += 1
        return result

    def _fitness(self, chrom: np.ndarray) -> float:
        r = self._sim(chrom)
        n = len(self.users)
        alloc_rate = len(r.allocated) / max(n, 1)
        avg_sat = (r.total_satisfaction / len(r.allocated)) if r.allocated else 0.0
        online_sv = [s for s in r.servers if s.is_online]
        if online_sv:
            utils = [s.utilization() for s in online_sv]
            bal = 1.0 - np.std(utils)
            avg_util = np.mean(utils)
        else:
            bal, avg_util = 0.0, 0.0
        hp = sum(1 for u in self.users if u.sla_sensitive)
        sla_pen = r.high_priority_violations / hp if hp > 0 else 0.0
        return float(np.clip(0.40*alloc_rate + 0.25*avg_sat + 0.20*bal + 0.15*avg_util - 0.35*sla_pen, 0, 1))

    def _new_chrom(self, rng) -> np.ndarray:
        c = np.full(self.n_users, -1, dtype=int)
        for i in range(self.n_users):
            if rng.rand() < 0.75:
                c[i] = rng.randint(0, self.n_servers)
        return c

    def evolve(self, progress_cb=None) -> Tuple[np.ndarray, float]:
        rng = np.random.RandomState(self.cfg.RANDOM_SEED)
        pop = [self._new_chrom(rng) for _ in range(self.cfg.GA_POPULATION_SIZE)]
        best_chrom, best_fit = None, -1.0
        cfg = self.cfg
        for gen in range(cfg.GA_GENERATIONS):
            fits = [self._fitness(c) for c in pop]
            gi = int(np.argmax(fits))
            if fits[gi] > best_fit:
                best_fit = fits[gi]
                best_chrom = pop[gi].copy()
            self.best_history.append(best_fit)
            self.avg_history.append(float(np.mean(fits)))
            if progress_cb:
                progress_cb(gen + 1, cfg.GA_GENERATIONS, best_fit, float(np.mean(fits)))
            # next gen
            elite_idx = np.argsort(fits)[-cfg.GA_ELITE_SIZE:]
            next_pop = [pop[i].copy() for i in elite_idx]
            while len(next_pop) < cfg.GA_POPULATION_SIZE:
                # tournament select
                ti = rng.choice(len(pop), cfg.GA_TOURNAMENT_SIZE, replace=False)
                p1 = pop[ti[int(np.argmax([fits[i] for i in ti]))]].copy()
                ti = rng.choice(len(pop), cfg.GA_TOURNAMENT_SIZE, replace=False)
                p2 = pop[ti[int(np.argmax([fits[i] for i in ti]))]].copy()
                # crossover
                if rng.rand() < cfg.GA_CROSSOVER_RATE:
                    pt1 = rng.randint(1, self.n_users - 1)
                    pt2 = rng.randint(pt1, self.n_users)
                    c1 = np.concatenate([p1[:pt1], p2[pt1:pt2], p1[pt2:]])
                    c2 = np.concatenate([p2[:pt1], p1[pt1:pt2], p2[pt2:]])
                else:
                    c1, c2 = p1, p2
                # mutate
                for c in [c1, c2]:
                    for i in range(len(c)):
                        if rng.rand() < cfg.GA_MUTATION_RATE:
                            c[i] = -1 if rng.rand() < 0.15 else rng.randint(0, self.n_servers)
                next_pop.extend([c1, c2])
            pop = next_pop[:cfg.GA_POPULATION_SIZE]
        return best_chrom, best_fit

    def get_result(self, chrom: np.ndarray) -> AllocationResult:
        return self._sim(chrom)


# ─────────────────────────────────────────────────────────────────────────────
# METRICS
# ─────────────────────────────────────────────────────────────────────────────

def compute_metrics(result: AllocationResult, users: List[User], cfg: Config) -> Dict:
    n = len(users)
    na = len(result.allocated)
    alloc_rate = 100 * na / max(n, 1)
    avg_sat = result.total_satisfaction / na if na > 0 else 0.0
    hp = sum(1 for u in users if u.sla_sensitive)
    sla = 100 * (1 - result.high_priority_violations / hp) if hp > 0 else 100.0
    online = [s for s in result.servers if s.is_online]
    if online:
        cpu_utils = [s.utilization() for s in online]
        mem_utils = [s.memory_utilization() for s in online]
        avg_cpu = 100 * np.mean(cpu_utils)
        avg_mem = 100 * np.mean(mem_utils)
        bal = float(1.0 - np.std(cpu_utils)) if len(cpu_utils) > 1 else 1.0
    else:
        avg_cpu = avg_mem = bal = 0.0
    wl_stats = {}
    uid_map = {u.id: u.workload_type for u in users}
    for wt in cfg.WORKLOAD_MIX:
        total = sum(1 for u in users if u.workload_type == wt)
        alloc = sum(1 for a in result.allocated if uid_map.get(a['user_id']) == wt)
        wl_stats[wt] = {'total': total, 'allocated': alloc,
                         'success_rate': 100 * alloc / max(total, 1)}
    return {'allocation_success_rate': alloc_rate, 'rejection_rate': 100 - alloc_rate,
            'avg_satisfaction': avg_sat, 'sla_compliance_rate': sla,
            'avg_cpu_utilization': avg_cpu, 'avg_mem_utilization': avg_mem,
            'cpu_balance_score': bal, 'high_priority_violations': result.high_priority_violations,
            'workload_stats': wl_stats, 'total_allocated': na,
            'total_rejected': len(result.rejected), 'online_servers': len(online)}


# ─────────────────────────────────────────────────────────────────────────────
# PLOTLY CHART HELPERS
# ─────────────────────────────────────────────────────────────────────────────

PLOT_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(15,22,41,0.6)',
    font=dict(family='DM Sans', color='#94a3b8', size=11),
    margin=dict(l=40, r=20, t=40, b=40),
    xaxis=dict(gridcolor='#1e2d4a', zerolinecolor='#1e2d4a'),
    yaxis=dict(gridcolor='#1e2d4a', zerolinecolor='#1e2d4a'),
)

C_FUZZY  = '#f87171'
C_HYBRID = '#34d399'
C_BLUE   = '#38bdf8'
C_AMBER  = '#fbbf24'


def chart_server_load(fuzzy_r: AllocationResult, hybrid_r: AllocationResult):
    sv_ids = [f"S{s.id}" for s in fuzzy_r.servers]
    f_cpu = [100 * s.utilization() for s in fuzzy_r.servers]
    h_cpu = [100 * s.utilization() for s in hybrid_r.servers]
    f_online = [s.is_online for s in fuzzy_r.servers]

    fig = go.Figure()
    fig.add_trace(go.Bar(name='Fuzzy Only', x=sv_ids, y=f_cpu, marker_color=C_FUZZY,
                         opacity=0.85, marker_line_width=0))
    fig.add_trace(go.Bar(name='Hybrid (GA)', x=sv_ids, y=h_cpu, marker_color=C_HYBRID,
                         opacity=0.85, marker_line_width=0))
    fig.add_hline(y=80, line_dash='dash', line_color=C_AMBER, annotation_text='80% threshold',
                  annotation_font_color=C_AMBER)
    fig.update_layout(**PLOT_LAYOUT, title='CPU Utilization per Server',
                       title_font=dict(color='#f1f5f9', size=13),
                       barmode='group', yaxis_range=[0, 110],
                       legend=dict(bgcolor='rgba(0,0,0,0)', font_color='#94a3b8'))
    # offline indicators
    for i, (sv, online) in enumerate(zip(sv_ids, f_online)):
        if not online:
            fig.add_annotation(x=sv, y=5, text='OFFLINE', showarrow=False,
                                font=dict(color='#f87171', size=9),
                                bgcolor='rgba(248,113,113,0.15)')
    return fig


def chart_ga_evolution(ga: GeneticAlgorithm):
    gens = list(range(1, len(ga.best_history) + 1))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=gens, y=ga.avg_history, name='Avg Fitness',
                              line=dict(color=C_AMBER, width=2, dash='dot'), fill='tozeroy',
                              fillcolor='rgba(251,191,36,0.05)'))
    fig.add_trace(go.Scatter(x=gens, y=ga.best_history, name='Best Fitness',
                              line=dict(color=C_HYBRID, width=2.5), fill='tozeroy',
                              fillcolor='rgba(52,211,153,0.08)'))
    fig.update_layout(**PLOT_LAYOUT, title='GA Evolution — Fitness over Generations',
                       title_font=dict(color='#f1f5f9', size=13),
                       xaxis_title='Generation', yaxis_title='Fitness',
                       legend=dict(bgcolor='rgba(0,0,0,0)', font_color='#94a3b8'))
    return fig


def chart_comparison_radar(fm: Dict, hm: Dict):
    cats = ['Allocation Rate', 'Satisfaction', 'SLA Compliance', 'CPU Balance', 'Mem Util']
    fv = [fm['allocation_success_rate'] / 100, fm['avg_satisfaction'],
          fm['sla_compliance_rate'] / 100, fm['cpu_balance_score'], fm['avg_mem_utilization'] / 100]
    hv = [hm['allocation_success_rate'] / 100, hm['avg_satisfaction'],
          hm['sla_compliance_rate'] / 100, hm['cpu_balance_score'], hm['avg_mem_utilization'] / 100]
    cats += [cats[0]]
    fv += [fv[0]]
    hv += [hv[0]]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=fv, theta=cats, fill='toself', name='Fuzzy Only',
                                   line_color=C_FUZZY, fillcolor='rgba(248,113,113,0.15)'))
    fig.add_trace(go.Scatterpolar(r=hv, theta=cats, fill='toself', name='Hybrid (GA)',
                                   line_color=C_HYBRID, fillcolor='rgba(52,211,153,0.15)'))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        polar=dict(
            bgcolor='rgba(15,22,41,0.6)',
            radialaxis=dict(visible=True, range=[0, 1], gridcolor='#1e2d4a', color='#64748b'),
            angularaxis=dict(gridcolor='#1e2d4a', color='#94a3b8'),
        ),
        font=dict(family='DM Sans', color='#94a3b8', size=11),
        margin=dict(l=40, r=40, t=40, b=40),
        title='Performance Radar',
        title_font=dict(color='#f1f5f9', size=13),
        legend=dict(bgcolor='rgba(0,0,0,0)', font_color='#94a3b8'),
    )
    return fig


def chart_workload_breakdown(fm: Dict, hm: Dict, cfg: Config):
    wl_types = list(cfg.WORKLOAD_MIX.keys())
    f_rates = [fm['workload_stats'][w]['success_rate'] for w in wl_types]
    h_rates = [hm['workload_stats'][w]['success_rate'] for w in wl_types]
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Fuzzy Only', x=wl_types, y=f_rates, marker_color=C_FUZZY, opacity=0.85))
    fig.add_trace(go.Bar(name='Hybrid (GA)', x=wl_types, y=h_rates, marker_color=C_HYBRID, opacity=0.85))
    fig.update_layout(**PLOT_LAYOUT, title='Success Rate by Workload Type',
                       title_font=dict(color='#f1f5f9', size=13),
                       barmode='group', yaxis_range=[0, 110],
                       yaxis_title='Success Rate (%)',
                       legend=dict(bgcolor='rgba(0,0,0,0)', font_color='#94a3b8'))
    return fig


def chart_satisfaction_dist(fr: AllocationResult, hr: AllocationResult):
    f_sat = [a['satisfaction'] for a in fr.allocated]
    h_sat = [a['satisfaction'] for a in hr.allocated]
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=f_sat, name='Fuzzy Only', nbinsx=25,
                                marker_color=C_FUZZY, opacity=0.7))
    fig.add_trace(go.Histogram(x=h_sat, name='Hybrid (GA)', nbinsx=25,
                                marker_color=C_HYBRID, opacity=0.7))
    fig.update_layout(**PLOT_LAYOUT, title='User Satisfaction Distribution',
                       title_font=dict(color='#f1f5f9', size=13),
                       barmode='overlay', xaxis_title='Satisfaction Score',
                       yaxis_title='Count',
                       legend=dict(bgcolor='rgba(0,0,0,0)', font_color='#94a3b8'))
    return fig


def chart_server_heatmap(result: AllocationResult, title: str):
    sv_ids = [s.id for s in result.servers]
    cpu_u = [s.utilization() for s in result.servers]
    mem_u = [s.memory_utilization() for s in result.servers]
    online = [1 if s.is_online else 0 for s in result.servers]
    z = [[c, m, o] for c, m, o in zip(cpu_u, mem_u, online)]
    fig = go.Figure(go.Heatmap(
        z=list(map(list, zip(*z))),
        x=[f"S{i}" for i in sv_ids],
        y=['CPU Util', 'Mem Util', 'Online'],
        colorscale='RdYlGn',
        zmin=0, zmax=1,
        showscale=True,
        colorbar=dict(tickfont=dict(color='#94a3b8'))
    ))
    fig.update_layout(**PLOT_LAYOUT, title=title,
                       title_font=dict(color='#f1f5f9', size=13))
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# UI HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def metric_card(label, value, color_cls, delta=None):
    delta_html = f'<div class="delta {color_cls}">{delta}</div>' if delta else ''
    return f"""
    <div class="metric-card">
        <div class="label">{label}</div>
        <div class="value {color_cls}">{value}</div>
        {delta_html}
    </div>"""


def improvement_badge(val):
    if val > 0:
        return f'<span style="color:#34d399;font-family:Space Mono;font-size:0.8rem">▲ +{val:.2f}</span>'
    elif val < 0:
        return f'<span style="color:#f87171;font-family:Space Mono;font-size:0.8rem">▼ {val:.2f}</span>'
    return f'<span style="color:#64748b;font-family:Space Mono;font-size:0.8rem">— {val:.2f}</span>'


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style="padding:1rem 0 0.5rem">
        <span style="font-family:Space Mono;font-size:1rem;font-weight:700;color:#38bdf8">⚡ SIM PARAMS</span>
    </div>""", unsafe_allow_html=True)

    st.markdown("**Infrastructure**")
    num_servers = st.slider("Servers", 6, 20, 12)
    num_users   = st.slider("Users", 100, 600, 300, step=50)
    fail_rate   = st.slider("Failure Rate", 0.0, 0.6, 0.30, step=0.05,
                            format="%.0f%%",
                            help="Probability each server fails")

    st.markdown("**GA Hyperparameters**")
    ga_gens  = st.slider("Generations", 10, 80, 40)
    ga_pop   = st.slider("Population", 30, 120, 60, step=10)
    ga_mut   = st.slider("Mutation Rate", 0.05, 0.25, 0.12, step=0.01)
    ga_cross = st.slider("Crossover Rate", 0.5, 1.0, 0.85, step=0.05)

    st.markdown("---")
    run_btn = st.button("▶  RUN SIMULATION", use_container_width=True)

    st.markdown("""
    <div style="margin-top:2rem;padding:0.8rem;background:#0a0e1a;border:1px solid #1e2d4a;border-radius:8px">
        <div style="font-family:Space Mono;font-size:0.65rem;color:#38bdf8;letter-spacing:0.1em;margin-bottom:0.4rem">ABOUT</div>
        <div style="font-size:0.75rem;color:#64748b;line-height:1.5">
        Compares greedy <b style="color:#f87171">Fuzzy Logic</b> vs 
        GA-optimised <b style="color:#34d399">Hybrid</b> approach for 
        cloud resource allocation under failure scenarios.
        </div>
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<div class="main-header">
    <h1>⚡ Cloud Resource Allocation System</h1>
    <p>Fuzzy Logic (Greedy) vs Hybrid Fuzzy + Genetic Algorithm — AWS-Style Failure Simulation</p>
    <span class="tag">Fuzzy Logic</span>
    <span class="tag">Genetic Algorithm</span>
    <span class="tag">SLA Management</span>
    <span class="tag">Failure Recovery</span>
    <span class="tag">Multi-Agent</span>
</div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# RUN SIMULATION
# ─────────────────────────────────────────────────────────────────────────────

if run_btn or 'sim_done' not in st.session_state:
    cfg = Config(
        NUM_SERVERS=num_servers,
        NUM_USERS=num_users,
        FAILURE_PROBABILITY=fail_rate,
        GA_GENERATIONS=ga_gens,
        GA_POPULATION_SIZE=ga_pop,
        GA_MUTATION_RATE=ga_mut,
        GA_CROSSOVER_RATE=ga_cross,
    )

    # Status
    status = st.empty()
    prog   = st.empty()
    msg    = st.empty()

    with status.container():
        st.markdown("""
        <div style="background:#0f1629;border:1px solid #1e3a5f;border-radius:8px;padding:1rem 1.5rem;margin-bottom:1rem">
            <span style="font-family:Space Mono;font-size:0.8rem;color:#38bdf8">⚙ INITIALISING SIMULATION...</span>
        </div>""", unsafe_allow_html=True)

    # Init
    users   = gen_users(cfg)
    servers = init_servers(cfg)
    fz      = FuzzyLogicController(cfg)

    # Failures
    fail_report = simulate_failures(servers, cfg)

    # Fuzzy-only
    msg.markdown(f'<p style="font-family:Space Mono;font-size:0.75rem;color:#64748b">🔴 Running Fuzzy-only greedy allocation...</p>', unsafe_allow_html=True)
    fuzzy_servers = [Server(s.id, s.cpu_capacity, s.mem_capacity, s.is_online,
                             s.current_cpu_load, s.current_mem_load) for s in servers]
    fuzzy_result  = fuzzy_only_allocation(users, fuzzy_servers, fz, cfg)
    fuzzy_metrics = compute_metrics(fuzzy_result, users, cfg)

    # GA
    msg.markdown(f'<p style="font-family:Space Mono;font-size:0.75rem;color:#64748b">🟢 Running Genetic Algorithm optimisation...</p>', unsafe_allow_html=True)
    pbar = prog.progress(0)

    ga_log = {'gen': [], 'best': [], 'avg': []}
    def progress_cb(gen, total, best, avg):
        pbar.progress(gen / total)
        ga_log['gen'].append(gen)
        ga_log['best'].append(best)
        ga_log['avg'].append(avg)

    hybrid_servers = [Server(s.id, s.cpu_capacity, s.mem_capacity, s.is_online,
                              s.current_cpu_load, s.current_mem_load) for s in servers]
    ga = GeneticAlgorithm(users, hybrid_servers, fz, cfg)
    best_chrom, best_fit = ga.evolve(progress_cb=progress_cb)
    hybrid_result  = ga.get_result(best_chrom)
    hybrid_metrics = compute_metrics(hybrid_result, users, cfg)

    # Store
    st.session_state.update({
        'sim_done': True, 'cfg': cfg, 'users': users, 'servers': servers,
        'fail_report': fail_report, 'fuzzy_result': fuzzy_result, 'fuzzy_metrics': fuzzy_metrics,
        'hybrid_result': hybrid_result, 'hybrid_metrics': hybrid_metrics, 'ga': ga,
        'best_fit': best_fit,
    })

    status.empty(); prog.empty(); msg.empty()

# ─────────────────────────────────────────────────────────────────────────────
# DISPLAY RESULTS
# ─────────────────────────────────────────────────────────────────────────────

if 'sim_done' in st.session_state:
    cfg      = st.session_state['cfg']
    users    = st.session_state['users']
    fr       = st.session_state['fuzzy_result']
    fm       = st.session_state['fuzzy_metrics']
    hr       = st.session_state['hybrid_result']
    hm       = st.session_state['hybrid_metrics']
    ga       = st.session_state['ga']
    fail_rep = st.session_state['fail_report']

    # ── Failure banner ──
    st.markdown(f"""
    <div style="background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.3);
                border-radius:8px;padding:0.7rem 1.2rem;margin-bottom:1.2rem;display:flex;align-items:center;gap:1rem">
        <span style="font-size:1.2rem">⚠️</span>
        <span style="font-family:Space Mono;font-size:0.78rem;color:#fca5a5">
            FAILURE EVENT — Primary: <b>{len(fail_rep['primary'])}</b> servers down &nbsp;|&nbsp;
            Cascade: <b>{len(fail_rep['cascade'])}</b> &nbsp;|&nbsp;
            Total: <b>{fail_rep['total']}/{cfg.NUM_SERVERS}</b> &nbsp;|&nbsp;
            Online: <b>{hm['online_servers']}</b>
        </span>
    </div>""", unsafe_allow_html=True)

    # ── Top KPI cards ──
    st.markdown('<div class="section-label">KEY PERFORMANCE INDICATORS</div>', unsafe_allow_html=True)

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    kpis = [
        (c1, "ALLOC RATE (Fuzzy)", f"{fm['allocation_success_rate']:.1f}%",
         f"Hybrid: {hm['allocation_success_rate']:.1f}%", "val-red"),
        (c2, "ALLOC RATE (Hybrid)", f"{hm['allocation_success_rate']:.1f}%",
         f"+{hm['allocation_success_rate']-fm['allocation_success_rate']:.1f}%", "val-green"),
        (c3, "SLA COMPLIANCE", f"{hm['sla_compliance_rate']:.1f}%",
         f"Fuzzy: {fm['sla_compliance_rate']:.1f}%", "val-green"),
        (c4, "SLA VIOLATIONS", str(hm['high_priority_violations']),
         f"Fuzzy had {fm['high_priority_violations']}", "val-blue"),
        (c5, "LOAD BALANCE", f"{hm['cpu_balance_score']:.3f}",
         f"Fuzzy: {fm['cpu_balance_score']:.3f}", "val-green"),
        (c6, "GA BEST FITNESS", f"{st.session_state['best_fit']:.4f}",
         f"{cfg.GA_GENERATIONS} gens", "val-amber"),
    ]
    for col, label, val, delt, cls in kpis:
        with col:
            st.markdown(metric_card(label, val, cls, delt), unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── Tabs ──
    tabs = st.tabs(["📊 Comparison", "🧬 GA Evolution", "🖥️ Server Analysis", "📦 Workloads", "📋 Data Table"])

    # ── Tab 1: Comparison ──
    with tabs[0]:
        col_l, col_r = st.columns([1, 1])
        with col_l:
            st.plotly_chart(chart_comparison_radar(fm, hm), use_container_width=True)
        with col_r:
            st.plotly_chart(chart_satisfaction_dist(fr, hr), use_container_width=True)

        st.plotly_chart(chart_server_load(fr, hr), use_container_width=True)

    # ── Tab 2: GA Evolution ──
    with tabs[1]:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.plotly_chart(chart_ga_evolution(ga), use_container_width=True)
        with col2:
            st.markdown('<div class="section-label">GA CONFIGURATION</div>', unsafe_allow_html=True)
            ga_params = {
                'Population Size': cfg.GA_POPULATION_SIZE,
                'Generations': cfg.GA_GENERATIONS,
                'Crossover Rate': f"{cfg.GA_CROSSOVER_RATE:.0%}",
                'Mutation Rate': f"{cfg.GA_MUTATION_RATE:.0%}",
                'Elite Size': cfg.GA_ELITE_SIZE,
                'Tournament Size': cfg.GA_TOURNAMENT_SIZE,
                'Final Best Fitness': f"{st.session_state['best_fit']:.4f}",
                'Initial Avg Fitness': f"{ga.avg_history[0]:.4f}" if ga.avg_history else "N/A",
                'Final Avg Fitness': f"{ga.avg_history[-1]:.4f}" if ga.avg_history else "N/A",
            }
            for k, v in ga_params.items():
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;padding:6px 0;
                            border-bottom:1px solid #1e2d4a;">
                    <span style="font-size:0.8rem;color:#64748b">{k}</span>
                    <span style="font-family:Space Mono;font-size:0.8rem;color:#38bdf8">{v}</span>
                </div>""", unsafe_allow_html=True)

    # ── Tab 3: Server Analysis ──
    with tabs[2]:
        col_f, col_h = st.columns(2)
        with col_f:
            st.markdown('<span class="badge-fuzzy">FUZZY ONLY</span>', unsafe_allow_html=True)
            st.plotly_chart(chart_server_heatmap(fr, "Fuzzy — Server State"), use_container_width=True)
        with col_h:
            st.markdown('<span class="badge-hybrid">HYBRID (GA)</span>', unsafe_allow_html=True)
            st.plotly_chart(chart_server_heatmap(hr, "Hybrid — Server State"), use_container_width=True)

        # Server table
        sv_rows = []
        for fs, hs in zip(fr.servers, hr.servers):
            sv_rows.append({
                'Server': f'S{fs.id}',
                'Capacity (CPU)': fs.cpu_capacity,
                'Online': '✅' if fs.is_online else '❌',
                'Fuzzy CPU%': f"{100*fs.utilization():.1f}",
                'Hybrid CPU%': f"{100*hs.utilization():.1f}",
                'Hybrid Mem%': f"{100*hs.memory_utilization():.1f}",
            })
        st.dataframe(pd.DataFrame(sv_rows), use_container_width=True, hide_index=True)

    # ── Tab 4: Workloads ──
    with tabs[3]:
        st.plotly_chart(chart_workload_breakdown(fm, hm, cfg), use_container_width=True)

        wl_rows = []
        for wt in cfg.WORKLOAD_MIX:
            fw = fm['workload_stats'][wt]
            hw = hm['workload_stats'][wt]
            wl_rows.append({
                'Workload': wt,
                'Total Users': fw['total'],
                'Fuzzy Allocated': fw['allocated'],
                'Fuzzy Rate': f"{fw['success_rate']:.1f}%",
                'Hybrid Allocated': hw['allocated'],
                'Hybrid Rate': f"{hw['success_rate']:.1f}%",
                'Δ Improvement': f"{hw['success_rate'] - fw['success_rate']:+.1f}%",
            })
        st.dataframe(pd.DataFrame(wl_rows), use_container_width=True, hide_index=True)

    # ── Tab 5: Data Table ──
    with tabs[4]:
        col_s = st.selectbox("View allocations for:", ["Hybrid (GA)", "Fuzzy Only"])
        result_to_show = hr if col_s == "Hybrid (GA)" else fr
        df_alloc = pd.DataFrame(result_to_show.allocated)
        if not df_alloc.empty:
            df_alloc['priority'] = df_alloc['priority'].round(3)
            df_alloc['satisfaction'] = df_alloc['satisfaction'].round(4)
            st.dataframe(df_alloc, use_container_width=True, hide_index=True)
            st.markdown(f"""<span style="font-family:Space Mono;font-size:0.75rem;color:#64748b">
                {len(df_alloc)} allocations shown | {len(result_to_show.rejected)} rejected</span>""",
                unsafe_allow_html=True)

    # ── Summary banner ──
    improvement = hm['allocation_success_rate'] - fm['allocation_success_rate']
    sla_saved   = fm['high_priority_violations'] - hm['high_priority_violations']
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,rgba(52,211,153,0.05),rgba(56,189,248,0.05));
                border:1px solid rgba(52,211,153,0.2);border-radius:10px;
                padding:1.2rem 1.8rem;margin-top:1.5rem;display:flex;gap:3rem;align-items:center">
        <div>
            <div style="font-family:Space Mono;font-size:0.65rem;color:#64748b;letter-spacing:0.1em">ALLOCATION GAIN</div>
            <div style="font-family:Space Mono;font-size:1.4rem;font-weight:700;color:#34d399">
                {improvement:+.2f}%
            </div>
        </div>
        <div>
            <div style="font-family:Space Mono;font-size:0.65rem;color:#64748b;letter-spacing:0.1em">SLA VIOLATIONS SAVED</div>
            <div style="font-family:Space Mono;font-size:1.4rem;font-weight:700;color:#38bdf8">
                {sla_saved}
            </div>
        </div>
        <div>
            <div style="font-family:Space Mono;font-size:0.65rem;color:#64748b;letter-spacing:0.1em">SATISFACTION DELTA</div>
            <div style="font-family:Space Mono;font-size:1.4rem;font-weight:700;color:#fbbf24">
                {hm['avg_satisfaction'] - fm['avg_satisfaction']:+.4f}
            </div>
        </div>
        <div style="margin-left:auto;font-size:0.78rem;color:#64748b;max-width:300px;line-height:1.6">
            Hybrid (Fuzzy + GA) outperforms greedy Fuzzy Logic by globally optimising 
            the chromosome across {cfg.GA_GENERATIONS} generations with a population of {cfg.GA_POPULATION_SIZE}.
        </div>
    </div>""", unsafe_allow_html=True)