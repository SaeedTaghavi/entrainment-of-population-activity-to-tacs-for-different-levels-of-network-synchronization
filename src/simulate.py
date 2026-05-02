"""
simulate.py — E-I network simulator with tACS (NEST-based)

Core simulation module for the paper:
  "Tuning the brain rhythms: How internal coherence influences
   network entrainment by tACS"
  Chaos, Solitons & Fractals (2025), doi:10.1016/j.chaos.2025.014341

Network: recurrent excitatory–inhibitory (E-I) spiking network
         built in NEST, driven by a sinusoidal AC current (tACS).

Usage
-----
    from src.simulate import simulate
    response = simulate(T=10000, ac_freq_ex=30, ac_amp_ex=6, ...)
    # response is a dict with spike times, population activity, etc.
"""

import time
import numpy as np
import os 

try:
    import nest
    NEST_AVAILABLE = True
except ImportError:
    NEST_AVAILABLE = False
    print("Warning: NEST not found. Simulation cannot run, but analysis utilities work.")



##### simulation params
RS_param = {
    "V_reset": -58.0,
    "V_peak": 0.0,
    "V_th": -50.0,
    "I_e": 0.0,
    "g_L": 10.0,
    "tau_w": 300.0,
    "E_L": -70.0,
    "Delta_T": 2.0,
    "a": 3.0,
    "b": 0.0,
    "C_m": 200.0,
    "V_m": -70.0,  #! must be equal to E_L
    "w": 5.0,  #! must be equal to 5.
    "t_ref": 1.0,
}

# fast spiking - no adaptation
FS_params = {
    "V_reset": -58.0,
    "V_peak": 0.0,
    "V_th": -50.0,
    "I_e": 0.0,
    "g_L": 10.0,
    "tau_w": 300.0,
    "E_L": -70.0,
    "Delta_T": 2.0,
    "a": 0.0,
    "b": 0.0,
    "C_m": 200.0,
    "V_m": -70.0,  #! must be equal to E_L
    "w": 5.0,  #! must be equal to 5.
    "t_ref": 1.0,
}
#######################


##### network
# the main code you need to simulate the network in nest
def simulate(
    itrial=False,
    tpert=False,
    phase=False,
    T=2000,
    dt=0.1,
    num_threads=os.cpu_count() - 2,
    ac_freq_ex=2.0,
    ac_amp_ex=1.0,
    ac_freq_in=2.0,
    ac_amp_in=1.0,
    num_neurons_ex=800,
    num_neurons_in=200,
    rate_input_ex=30000,
    rate_input_in=30000,
    we_mean=1.0,
    wi_mean=1.0,
    we_std=0.1,
    wi_std=0.1,
    tau_synEx_popIn=5.0,
    tau_synIn_popIn=3.0,
    tau_synEx_popEx=5.0,
    tau_synIn_popEx=3.0,
    pee=0.4,
    pei=0.5,
    pie=0.5,
    pii=0.5,
    wee_mean=3.0,
    wei_mean=3.0,
    wie_mean=3.0,
    wii_mean=3.0,
    wee_std=1.0,
    wei_std=1.0,
    wie_std=1.0,
    wii_std=1.0,
    dee_mean=3,
    dei_mean=3,
    die_mean=3,
    dii_mean=3,
    dee_std=0.01,
    dei_std=0.01,
    die_std=0.01,
    dii_std=0.01,
):

    param_in = FS_params
    param_ex = FS_params
    input_params = {  # I need these parameters to reproduce results
        "T": T,
        "dt": dt,
        "num_neurons_in": num_neurons_in,
        "num_neurons_ex": num_neurons_ex,
        "rate_input_ex": rate_input_ex,
        "rate_input_in": rate_input_in,
        "we_mean": we_mean,
        "wi_mean": wi_mean,
    }

    ########## pipeline - 1 - setup nest
    nest.ResetKernel()
    nest.set_verbosity(100)
    nest.SetKernelStatus(
        {"local_num_threads": num_threads, "resolution": dt, "rng_seed": 1}
    )
    if itrial:
        nest.SetKernelStatus(
            {"local_num_threads": num_threads, "resolution": dt, "rng_seed": itrial + 1}
        )

    ########## pipeline - 2 - create populations
    pop_ex = nest.Create("aeif_psc_exp", n=num_neurons_ex, params=param_ex)
    pop_ex.set(
        {"V_m": nest.random.uniform(min=param_ex["V_reset"], max=param_ex["V_th"])}
    )
    pop_ex.set({"tau_syn_ex": tau_synEx_popEx})
    pop_ex.set({"tau_syn_in": tau_synIn_popEx})

    pop_in = nest.Create("aeif_psc_exp", n=num_neurons_in, params=param_in)
    pop_in.set(
        {"V_m": nest.random.uniform(min=param_in["V_reset"], max=param_in["V_th"])}
    )
    pop_in.set({"tau_syn_ex": tau_synEx_popIn})
    pop_in.set({"tau_syn_in": tau_synIn_popIn})
    print(nest.GetStatus(pop_ex[0]))
    print(nest.GetStatus(pop_in[0]))
    # .set({"C_m": 100})

    ########## pipeline - 3 - create stimulations
    pg_popEx = nest.Create(
        "poisson_generator",
        num_neurons_ex,
        params={
            "rate": nest.math.redraw(
                nest.random.normal(mean=rate_input_ex, std=500), min=0.0, max=np.inf
            ),
        },
    )
    pg_popIn = nest.Create(
        "poisson_generator",
        num_neurons_in,
        params={
            "rate": nest.math.redraw(
                nest.random.normal(mean=rate_input_in, std=500), min=0.0, max=np.inf
            ),
        },
    )
    # pg_popEx = nest.Create(
    #     "poisson_generator",
    #     num_neurons_ex,
    #     params={
    #         "rate": nest.random.uniform(
    #             min=rate_input_ex - 500, max=rate_input_ex + 500
    #         ),
    #     },
    # )
    # pg_popIn = nest.Create(
    #     "poisson_generator",
    #     num_neurons_in,
    #     params={
    #         "rate": nest.random.uniform(
    #             min=rate_input_in - 500, max=rate_input_in + 500
    #         ),
    #     },
    # )

    ac_ex = nest.Create(
        "ac_generator",
        1,
        params={
            "amplitude": ac_amp_ex,
            "frequency": ac_freq_ex,
            "start": 1000,
        },
    )

    ac_in = nest.Create(
        "ac_generator",
        1,
        params={
            "amplitude": ac_amp_in,
            "frequency": ac_freq_in,
            "start": 1000,
        },
    )

    if phase:
        # Phase of the external ac current (0-360 deg)
        ac_ex.set(phase=phase)
        ac_in.set(phase=phase)

    ########## pipeline - 4 - create recording devices
    sr_in = nest.Create("spike_recorder", params={"start": 0})
    sr_ex = nest.Create("spike_recorder", params={"start": 0})

    mm_ex = nest.Create(
        "multimeter",
        params={"record_from": ["I_syn_ex", "I_syn_in", "V_m", "w"], "start": 0},
    )
    mm_in = nest.Create(
        "multimeter",
        params={"record_from": ["I_syn_ex", "I_syn_in", "V_m", "w"], "start": 0},
    )
    mm_ac_ex = nest.Create(
        "multimeter", params={"record_from": ["I"], "start": 1000, "interval": 0.1}
    )
    mm_ac_in = nest.Create(
        "multimeter", params={"record_from": ["I"], "start": 1000, "interval": 0.1}
    )

    ########## pipeline - 5 - connect
    nest.Connect(ac_ex, pop_ex)
    nest.Connect(ac_in, pop_in)

    nest.Connect(
        pg_popEx,
        pop_ex,
        "one_to_one",
        syn_spec={
            "weight": nest.math.redraw(
                nest.random.normal(mean=we_mean, std=we_std), min=0.0, max=100.0
            ),
        },
    )
    nest.Connect(
        pg_popIn,
        pop_in,
        "one_to_one",
        syn_spec={
            "weight": nest.math.redraw(
                nest.random.normal(mean=wi_mean, std=wi_std), min=0.0, max=100.0
            ),
        },
    )

    if tpert:
        dc = nest.Create("dc_generator", 1)
        dc.set(amplitude=100, start=tpert, stop=tpert + 10 * dt)
        nest.Connect(dc, pop_ex, "all_to_all")

    conn_spec_ee = {
        "rule": "pairwise_bernoulli",
        "p": pee,
    }
    conn_spec_ei = {
        "rule": "pairwise_bernoulli",
        "p": pei,
    }
    conn_spec_ie = {
        "rule": "pairwise_bernoulli",
        "p": pie,
    }
    conn_spec_ii = {
        "rule": "pairwise_bernoulli",
        "p": pii,
    }

    syn_spec_ee = {
        "weight": nest.math.redraw(
            nest.random.normal(mean=wee_mean, std=wee_std),
            min=0.0,
            max=100.0,
        ),
        "delay": nest.math.redraw(
            nest.random.normal(mean=dee_mean, std=dee_std), min=0.1, max=100.0
        ),
    }

    syn_spec_ei = {
        "weight": nest.math.redraw(
            nest.random.normal(mean=wei_mean, std=wei_std),
            min=0.0,
            max=100.0,
        ),
        "delay": nest.math.redraw(
            nest.random.normal(mean=dei_mean, std=dei_std), min=0.1, max=100.0
        ),
    }

    syn_spec_ie = {
        "weight": nest.math.redraw(
            nest.random.normal(mean=-wie_mean, std=wie_std), min=-100.0, max=0.0
        ),
        "delay": nest.math.redraw(
            nest.random.normal(mean=die_mean, std=die_std), min=0.1, max=100.0
        ),
    }

    syn_spec_ii = {
        "weight": nest.math.redraw(
            nest.random.normal(mean=-wii_mean, std=wii_std), min=-100.0, max=0.0
        ),
        "delay": nest.math.redraw(
            nest.random.normal(mean=dii_mean, std=dii_std), min=0.1, max=100.0
        ),
    }

    nest.Connect(pop_ex, pop_ex, conn_spec=conn_spec_ee, syn_spec=syn_spec_ee)
    nest.Connect(pop_ex, pop_in, conn_spec=conn_spec_ei, syn_spec=syn_spec_ei)
    nest.Connect(pop_in, pop_ex, conn_spec=conn_spec_ie, syn_spec=syn_spec_ie)
    nest.Connect(pop_in, pop_in, conn_spec=conn_spec_ii, syn_spec=syn_spec_ii)

    nest.Connect(mm_ex, pop_ex)
    nest.Connect(mm_in, pop_in)
    nest.Connect(pop_in, sr_in)
    nest.Connect(pop_ex, sr_ex)

    nest.Connect(mm_ac_ex, ac_ex)
    nest.Connect(mm_ac_in, ac_in)

    ########## pipeline - 6 - simulate
    nest.Simulate(T)
    response = {
        "input_params": input_params,
        "sr_in": sr_in.events,
        "mm_in": mm_in.events,
        "sr_ex": sr_ex.events,
        "mm_ex": mm_ex.events,
        "mm_ac_ex": mm_ac_ex.events,
        "mm_ac_in": mm_ac_in.events,
        "pg_popEx_rate": pg_popEx.rate,
        "pg_popIn_rate": pg_popIn.rate,
    }
    return response


