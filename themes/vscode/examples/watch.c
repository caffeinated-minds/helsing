#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>

#define ARRAY_LENGTH(items) (sizeof(items) / sizeof((items)[0]))

enum threat_level {
  THREAT_CLEAR,
  THREAT_OBSERVED,
  THREAT_SEVERE,
};

struct reading {
  const char *location;
  unsigned int shadows;
  bool invited;
};

static const char *const threat_names[] = {
    [THREAT_CLEAR] = "clear",
    [THREAT_OBSERVED] = "observed",
    [THREAT_SEVERE] = "severe",
};

static enum threat_level classify(const struct reading *reading) {
  if (reading->invited) {
    return THREAT_CLEAR;
  }
  if (reading->shadows >= 3U) {
    return THREAT_SEVERE;
  }
  return reading->shadows > 0U ? THREAT_OBSERVED : THREAT_CLEAR;
}

int main(void) {
  const struct reading patrol[] = {
      {.location = "library", .shadows = 0U, .invited = true},
      {.location = "crypt", .shadows = 4U, .invited = false},
  };

  for (size_t i = 0; i < ARRAY_LENGTH(patrol); ++i) {
    const enum threat_level level = classify(&patrol[i]);
    printf("%-8s %s\n", threat_names[level], patrol[i].location);
  }

  return 0;
}
