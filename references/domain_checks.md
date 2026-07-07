# Domain-Specific Review Checklists

Load only the relevant subsection during review.

## General machine learning

- Are training, validation, and test examples clearly separated?
- Are hyperparameters selected without test feedback?
- Are standard, strong, and compute-matched baselines included?
- Are improvements paired with variance, confidence intervals, or tests where sample-level pairing exists?
- Is preprocessing fit only on training data?
- Are claimed effects robust to seeds, dataset splits, and key ablations?
- Is the reported metric aligned with the task claim?

## LLM, RAG, retrieval, and memory

- Does any memory include test answers, documents, entities, prompts, retrieved passages, annotations, or near duplicates?
- How are candidate answers, evidence labels, and risk scores produced at construction and inference time?
- Are target benchmark development data or labels used to tune thresholds, prompts, retrievers, context budgets, or memory parameters?
- Are oracle and non-oracle variants sharply defined, including every privileged input?
- Are final generation, verification, attribution, retries, debate rounds, reranking, batching, latency, and token costs accounted for consistently?
- Do methods share comparable LLM backbones, decoding, retrieval corpus, top-K, context length, and test-time tools?
- Are correctness, faithfulness, harmful exposure, abstention, and cost separately defined and measured?

## LLM agents and multi-agent systems

- Is each protocol’s action space and routing information defined at decision time?
- Does a router access final test feedback, future execution results, or hidden evaluator signals?
- Are comparisons call-matched and budget-matched?
- Are outcomes paired across protocols under comparable stochasticity?
- Are agent roles, handoff context, retries, prompts, and stopping policies specified?
- Does a causal claim identify an intervention and plausible assumptions rather than relabeling correlation as causality?

## Time series, transfer learning, causal mechanism modeling

- Are domains, sensors, labels, time windows, and train/dev/test periods disjoint where needed?
- Is temporal leakage prevented in normalization, windowing, and random splitting?
- Are causal factors, domain factors, and nuisance factors operationally distinguishable?
- Are interventional/counterfactual claims supported by real interventions, a well-specified simulator, or clearly labeled synthetic perturbations?
- Are graph edges stable, uncertainty-calibrated, and validated beyond visual plausibility?
- Does cross-domain adaptation preserve target-only evaluation integrity?

## Embodied AI and robotics

- Are training scenes, validation scenes, test scenes, objects, maps, and episodes separated?
- Does the method receive privileged state, oracle maps, future observations, ground-truth pose, or simulator-only signals unavailable to baselines?
- Are navigation/action budgets, reset rules, collision costs, and success criteria consistent?
- Is the method practical under simulator, memory, latency, and compute constraints?
- Are claims about real-world transfer clearly separated from simulation evidence?

## Theory, causality, and guarantees

- Are assumptions stated before the theorem or guarantee?
- Does the theorem answer the central method claim rather than an idealized side case?
- Are estimands and interventions precisely defined?
- Are identifiability conditions plausible for the data observed?
- Are empirical results framed as validation, illustration, or proof appropriately?
