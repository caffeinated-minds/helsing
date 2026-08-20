type ThreatLevel = "clear" | "observed" | "severe";

interface Observation {
  readonly id: string;
  subject: string;
  shadows: number;
  recordedAt?: Date;
}

interface StoredObservation extends Observation {
  level: ThreatLevel;
  recordedAt: Date;
}

const thresholds = {
  observed: 1,
  severe: 3,
} as const;

class Registry<T extends { id: string }> {
  readonly #entries = new Map<string, T>();

  add(entry: T): void {
    this.#entries.set(entry.id, entry);
  }

  find(id: string): T | undefined {
    return this.#entries.get(id);
  }
}

function classify(shadows: number): ThreatLevel {
  if (shadows >= thresholds.severe) return "severe";
  if (shadows >= thresholds.observed) return "observed";
  return "clear";
}

export async function register(
  registry: Registry<StoredObservation>,
  observation: Observation,
): Promise<StoredObservation> {
  await Promise.resolve();

  const stored = {
    ...observation,
    level: classify(observation.shadows),
    recordedAt: observation.recordedAt ?? new Date(),
  } satisfies StoredObservation;

  registry.add(stored);
  return stored;
}
