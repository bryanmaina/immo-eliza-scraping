## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure in `src/`
- [ ] T002 Initialize Python project with `requirements.txt` including
      `selenium` and `pandas`
- [ ] T003 Configure linting and formatting tools( black)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can
be implemented

- [ ] T004 Configure logging and hydra
- [ ] T005 Implement error handling and retry mechanism in
      `src/error_handling.py`
- [ ] T006 Create the core scraper service in `src/scraper_service.py`

---

## Phase 3: User Story 1 - Scrape Property Data (Priority: P1) 🎯 MVP

**Goal**: Scrape property data from Belgian real estate websites and save it to
a CSV file.

### Implementation for User Story 1

- [ ] T007 Implement scraper for Immoweb in
      `src/scrapers/immoweb_scraper.py`
- [ ] T008 Implement scraper for Zimmo in
      `src/scrapers/zimmo_scraper.py`
- [ ] T009  Implement scraper for Realo in
      `src/scrapers/realo_scraper.py`
- [ ] T010  Implement data processing and cleaning in
      `src/data_processing.py`
- [ ] T011  Implement CSV export functionality in `src/csv_exporter.py`
- [ ] T012  Create the main CLI script in `src/main.py` that orchestrates
      the scraping process

---

## Phase : Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T016  Add documentation for the project in `README.md`
- [ ] T017 Code cleanup and refactoring
