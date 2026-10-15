# P6 Integration Patch and Independent Rerun

**Responsible author:** Qussai Adlbi

## MyoSim integration change
The downstream P6 run uses a general-purpose MyoSim configuration field:

```yaml
control:
  confirmation_policy: single_event
```

The default remains `multi_window`; existing configurations are unchanged. The new option is validated by the configuration object and handled by the state machine. A single accepted authenticated discrete event can release a command, while chronology checks, confidence gating, safety limiting, and emergency-stop behavior remain active.

The modified implementation files used for the run are:

- `src/myosim/core/config.py`
- `src/myosim/control/state_machine.py`

The engineering checks passed: **19 MyoSim unit/integration tests**, the new single-event fixture, and the default multi-window compatibility fixture.

## Independent rerun
The complete downstream run was copied to an independent output directory and replayed with the same data, code, configuration, seed, and task contract. All 60 records matched the primary run exactly when parsed as JSON.

- Primary runs: 60
- Independent rerun runs: 60
- Exact parsed-record match: true
- Invalid states: 0 in both runs
- Successful pick-place outcomes: 0 in both runs

This patch validates the integration pathway. It does not change the scientific interpretation: the downstream result is negative/inconclusive for a quality-to-task-utility association.
