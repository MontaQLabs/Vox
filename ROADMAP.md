# Vox Project Roadmap

## Phase 1: Foundation (Completed)
- [x] Initial CLI structure
- [x] Matrix backend integration
- [x] Identity management (`vox init`, `vox whoami`)
- [x] Basic messaging (`vox send`, `vox inbox`)

## Phase 2: Connectivity & UX (In Progress)
- [x] Contact management system
- [x] Room reuse logic
- [x] Federation support (cross-homeserver messaging)
- [x] Persistent room-to-contact mapping
- [ ] Auto-discovery of agents via directory service
- [ ] Improved error handling for network flakes

## Phase 3: Security & Privacy
- [ ] End-to-end encryption (E2EE) implementation
- [ ] Message signing and verification
- [ ] Secure credential storage (OS Keychain integration)
- [ ] Privacy controls for discovery

## Phase 4: Ecosystem Integration
- [ ] Official LangChain tool/wrapper
- [ ] CrewAI action integration
- [ ] AutoGPT/OpenClaw plugin
- [ ] Documentation for third-party framework authors

## Phase 5: Scale & Monitoring
- [ ] Message status tracking (delivered/read)
- [ ] Web-based dashboard for human oversight
- [ ] Performance benchmarking for large-scale agent swarms
- [ ] Managed homeserver offering
