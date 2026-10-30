# Devin quota ranking: live validation (test phase, ce8b9a69)

Every scenario ran the real `bin/fm-dispatch-resolve.sh` from the gate worktree in a disposable
lab home (`bin/fm-lab-home.sh create`). Quota evidence came from the real `quota-axi` 0.1.67,
answering from a disposable cache-format snapshot via `QUOTA_AXI_SNAPSHOT`, which never reads vendor credentials.
Rule choice came from a disposable local System One endpoint (`FM_DISPATCH_PROVIDER=systemone`, 127.0.0.1).

| File | Scenario |
| --- | --- |
| s1-healthy-included-priced-escalates.txt | Priced Fusion line wins included_quota ranking -> escalate with the approval reason, no profile line |
| s2-exhausted-included-free-stays-eligible.txt | included_quota exhausted_now -> Free swe-2-medium and modelless stay eligible; priced vetoed; clears to claude:sonnet |
| s3-adversarial-priced-gate.txt | Priced alone, provider-prefixed id, case-variant Free id, preferred_provider devin -> all escalate |
| s3f-devin-not-in-snapshot.txt | Devin unmeasured -> every devin line unranked, never cleared |
| s4-native-exhausted-and-free-only.txt | Native Claude exhausted -> priced still escalates; Free-only rule -> eligible+unranked, escalates "no rankable", never vetoed |
| s5-shared-quota-home.txt | shared_quota: Free first clears devin swe-2-medium; priced-first and modelless-first escalate; no quota-axi call |
| s6-quota-choose-frozen-map.txt | fm-quota-choose.sh refuses devin: identically at base and change |
| s7-before-after-devin-provider-map.txt | Base exits 2 (provider: devin required); change resolves via the devin -> devin map |
