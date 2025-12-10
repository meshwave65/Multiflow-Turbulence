# multiflux_jhtdb_validation.py
# Run this on JHU cluster with personal token – November 2025
# Author: Diógenes Duarte Sobral + Johns Hopkins Turbulence Team (co-authors)

import numpy as np, h5py, time, os
from sklearn.cluster import MiniBatchKMeans
from scipy.stats import linregress
from jhtdb import get_cutout  # JHTDB internal function

token = "YOUR_PERSONAL_TOKEN_HERE"
cases = [550, 950, 2000]

results = {}
for re in cases:
    print(f"\n=== Reτ = {re} ===")
    # Full field or large cutout (internal access)
    u = get_cutout(token, 'channel', time=0.0 if re==550 else 10.0 if re==950 else 20.0,
                   field='u', shape=(2048,512,1536) if re>550 else (1536,384,768))
    v = get_cutout(token, 'channel', time=..., field='v', shape=...)
    w = get_cutout(token, 'channel', time=..., field='w', shape=...)

    X = np.stack([u.ravel(), v.ravel(), w.ravel()], axis=1)
    clusterer = MiniBatchKMeans(n_clusters=12, batch_size=100000, random_state=42)
    labels = clusterer.fit_predict(X)

    # C_f drop
    u_ctrl = u.copy()
    for k in range(12):
        mask = labels.reshape(u.shape) == k
        v[mask] = v[mask].mean()
        w[mask] = w[mask].mean()

    tau_orig = np.mean(np.abs(np.gradient(u[:,0,:], axis=0)))
    tau_ctrl = np.mean(np.abs(np.gradient(u_ctrl[:,0,:], axis=0)))
    drop = (tau_orig - tau_ctrl) / tau_orig * 100

    results[re] = drop
    print(f"Reτ {re} → C_f drop = {drop:.1f}%")

print("\nFINAL VERDICT")
if np.mean(list(results.values())) > 35:
    print("TEORIA VIVA – MULTIFLUX VALIDATED")
else:
    print("Teoria refutada")
