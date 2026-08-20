// Package sentinel classifies unusual activity reported during daylight patrols.
package sentinel

import (
	"context"
	"fmt"
	"log"
	"time"
)

type ThreatLevel string

const (
	ThreatUnknown  ThreatLevel = "unknown"
	ThreatObserved ThreatLevel = "observed"
	ThreatSevere   ThreatLevel = "severe"
)

type Sighting struct {
	Subject   string
	Level     ThreatLevel
	Observed  time.Time
	Confirmed bool
}

type Repository interface {
	Recent(ctx context.Context, since time.Time) ([]Sighting, error)
}

type Watcher struct {
	repository Repository
	interval   time.Duration
}

func (w *Watcher) Patrol(ctx context.Context) error {
	since := time.Now().Add(-w.interval)
	sightings, err := w.repository.Recent(ctx, since)
	if err != nil {
		return fmt.Errorf("read recent sightings: %w", err)
	}

	for _, sighting := range sightings {
		if sighting.Confirmed && sighting.Level == ThreatSevere {
			log.Printf("warning: close the curtains near %s", sighting.Subject)
		}
	}

	return nil
}
