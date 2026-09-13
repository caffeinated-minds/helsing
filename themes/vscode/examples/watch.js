const MAX_SHADOWS = 3;

export class DaylightWatch {
  constructor(location) {
    this.location = location;
  }

  classify(shadows) {
    return shadows >= MAX_SHADOWS ? "severe" : "clear";
  }
}

export function inspect(location, shadows) {
  const watch = new DaylightWatch(location);
  return { location, level: watch.classify(shadows) };
}
