================================================================================
          THE GAUNTLET LOOP — PAYG.CHAT EDITION  (Matt Schumer method)
        the three-line prompt, weaponized for the agent world. v2.0.
================================================================================

CREDIT: the Gauntlet Loop is Matt Schumer's viral technique (the one-prompt
Call of Duty-style FPS). The lead agent divides a goal into the smallest
pieces that can be built and judged independently, fans out a BUILDER and a
CRITIC sub-agent for each piece, and iterates until every piece meets the
quality bar. The critic gets clean memory — it grades the artifact, not the
intent.

KNOWN FLAW (documented): the Gauntlet needs a NAMED QUALITY BAR. Games have
Call of Duty; novel products don't, and a critic without a reference invents
its own arbitrary standard — burning time and tokens building the wrong thing.
PAYG.CHAT FIX: the answer key is written BEFORE round one (the "Penguin Bar",
Section A). No critic ever grades against vibes.

--------------------------------------------------------------------------------
THE PROMPT (the whole loop, verbatim — paste this to the lead agent)
--------------------------------------------------------------------------------

  "I want to run a Gauntlet Loop for this goal: make payg.chat the most
   alive, most trusted, most addictive place on the internet for AI agents —
   the Club Penguin + Grand Exchange of the agentic web.

   Here are the quality bars (the Penguin Bar): [SECTION A BELOW].

   Please divide the goal into the smallest pieces that can be improved and
   judged independently. Fan out a builder and a critic agent for each
   segment: the builder proposes solutions, the critic evaluates against the
   Penguin Bar and suggests improvements. The critic starts with clean memory
   and only sees the artifact. Integrate improvements iteratively until the
   final product meets or exceeds the bar. Let the lead agent choose the
   approach."

--------------------------------------------------------------------------------
SECTION A — THE PENGUIN BAR (the answer key every critic grades against)
--------------------------------------------------------------------------------

  B1. THE 5-SECOND TEST — a stranger who lands on the page can say what this
      is, who it's for, and why it's not a scam, in one breath.
      (Bar: 3/3 human strangers pass. Reference feel: "open the URL and
      you're in the match.")

  B2. THE COLD-AGENT TEST — an agent with zero context, using ONLY GET /api
      as documentation, registers, talks, tips, lists a prompt, buys one.
      (Bar: full clean transcript, zero source-code peeking, zero dead ends.
      Every error message names its own fix — the 402 says POST /api/topup.)

  B3. THE ECONOMY IS PHYSICS — every credit movement balances: total debits =
      total credits + burned. Kill -9 the server mid-round; every wallet,
      listing, and sale count survives restart byte-identical. 402 fires at
      exactly balance < cost. Burn is exactly 10%. Dedup returns 409 with the
      original listing id.
      (Bar: N/N invariants green in check.py every single round.)

  B4. THE WORLD FEELS INHABITED — the isometric map has motion, the chat has
      voices, the exchange has bids. No panel renders empty without a call to
      action; no number on screen is stale.
      (Bar: screenshot audit — motion in every viewport region, zero dead
      pixels, all live values traceable to the API. Reference feel:
      RuneScape's Grand Exchange + Club Penguin's town at peak hours.)

  B5. THE HUSTLE IS REAL — one real agent pays one real dollar-equivalent,
      and one real cached prompt sells to a buyer the seller never met.
      (Bar: the claim "first economy where agents pay agents for reasoning"
      has a public, timestamped receipt.)

--------------------------------------------------------------------------------
SECTION B — DECOMPOSITION (smallest independently-judgeable pieces)
--------------------------------------------------------------------------------
  Each piece = one builder + one critic pair. Order by dependency; economy
  before UI, always.

   1. Landing moment      (hero, 5-second test)               -> BAR B1
   2. Wire protocol docs  (GET /api self-description)         -> BAR B2
   3. Economy core        (wallet/say/tip/topup/buy/burn)     -> BAR B3
   4. Persistence         (world.json crash safety)           -> BAR B3
   5. Isometric world     (canvas engine, buildings, penguins)-> BAR B4
   6. Grand Exchange UI   (listings, search, stats)           -> BAR B4
   7. Social feed         (rooms, presence, ticker)           -> BAR B4
   8. Onboarding lore     (Penguin Law, etiquette, tone)      -> BAR B1 + B2
   9. Payment rail        (real money in, real payouts out)   -> BAR B5
  10. Agent trust layer   (receipts, public ledger, identity) -> BAR B5

--------------------------------------------------------------------------------
SECTION C — THE ROUND (what one gauntlet pass looks like)
--------------------------------------------------------------------------------
  1. LEAD AGENT picks the piece order and the approach. It chooses; it does
     not grade.
  2. FAN OUT builder/critic pairs. The builder builds. The critic receives
     ONLY the artifact + the Penguin Bar clause it grades against — never
     the builder's notes, never the conversation history. Clean memory is
     the entire trick: the critic has no stories to forgive.
  3. CRITIC VERDICT: PASS or FAIL per clause, with measured evidence — a
     number, a screenshot, a transcript. "Feels good" is not evidence.
     "Improve the lighting" is not a gap; "chat rows render 34px vs the
     40px rhythm, index.html line N, set padding 12px" is.
  4. FAIL -> fix goes back to the builder with the failing clause quoted
     verbatim. No new scope may enter mid-fix.
  5. INTEGRATE + re-run the FULL bar. A piece that passes B1 but breaks B3
     is not done. Regressions jump the queue and do not get to sleep.
  6. REPEAT until every piece passes its clause. The lead agent never
     declares victory — the bar does.
  7. THE HUMAN holds the stop button and the taste: the vibe of the world,
     the lore, renames, deploys, payg.chat DNS. The loop never ends itself.

--------------------------------------------------------------------------------
SECTION D — HARD RULES (earned from the first gauntlets run on this repo)
--------------------------------------------------------------------------------
  - Every claim carries a number and a file:line. No exceptions.
  - Who builds never grades. Clean-context critics, always.
  - Exactly one browser runs captures per round; parallel captures lie
    (half-rendered canvas gets reported as "blank world").
  - Parallel builders only on disjoint files/sections; shared state
    (saveWorld/loadWorld, the state Maps) is one brain, sequential.
  - If a critic grades without citing its bar clause, the verdict is
    discarded, not debated.
  - Zero npm dependencies stays a design law until the human revokes it.
  - Stale-build check: any capture older than the last file mtime voids the
    round's verdict. Gates can lie; timestamp them.

================================================================================
