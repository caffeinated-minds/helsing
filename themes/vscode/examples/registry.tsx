import type { ReactNode } from "react";

type Observation = {
  id: string;
  subject: string;
  level: "clear" | "observed" | "severe";
};

interface ObservationCardProps {
  observation: Observation;
  children?: ReactNode;
}

export function ObservationCard({
  observation,
  children,
}: ObservationCardProps) {
  return (
    <article data-level={observation.level}>
      <h2>{observation.subject}</h2>
      {children}
    </article>
  );
}
