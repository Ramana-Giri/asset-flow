## DB Hardening (post-MVP)
- [ ] assets table: enforce status/assigned_to consistency at DB level 
      (currently possible to set status='assigned' with assigned_to=NULL, or vice versa)
      Likely fix: CHECK constraint comparing both columns, or a trigger.

## Asset Directory (post-MVP)
- [ ] Modify asset (edit details)
- [ ] Delete asset