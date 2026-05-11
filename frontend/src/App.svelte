<script>
  import TrendChart from './components/TrendChart.svelte'
  import raw from './data/houston_data.json'

  const TIER_COLOR = { High: '#e63946', Medium: '#f4a261', Low: '#2a9d8f' }
  const TIER_LABEL = {
    High: 'High AI Exposure',
    Medium: 'Medium AI Exposure',
    Low: 'Low AI Exposure',
  }

  const industriesMap = Object.fromEntries(raw.industries.map(i => [i.NAICS_3digit, i]))
  const trendMap = {}
  for (const row of raw.industry_trend) {
    trendMap[row.NAICS_3digit] = trendMap[row.NAICS_3digit] || []
    trendMap[row.NAICS_3digit].push(row)
  }

  const industries = [...raw.industries].sort((a, b) => a.Industry.localeCompare(b.Industry))

  let selected = ''
  let data = null

  function onSelect() {
    if (!selected) return
    const info = industriesMap[selected]
    const trend = (trendMap[selected] || []).sort((a, b) => a.Year - b.Year)
    data = { info, trend, tier_trend: raw.tier_trend }
  }

  $: tier = data?.info?.AI_Tier
  $: score = data?.info?.AI_Exposure_Score
  $: tierColor = tier ? TIER_COLOR[tier] : '#ccc'
</script>

<main>
  <header>
    <h1>Houston AI Exposure Explorer</h1>
    <p class="subtitle">
      Select your industry to see how exposed it is to AI — and how wages and
      employment have shifted from 2022 to 2024.
    </p>
  </header>

  <section class="selector">
    <label for="industry">Choose your industry</label>
    <select id="industry" bind:value={selected} on:change={onSelect}>
      <option value="">-- Select an industry --</option>
      {#each industries as ind}
        <option value={ind.NAICS_3digit}>{ind.Industry}</option>
      {/each}
    </select>
  </section>

  {#if data}
    <section class="result">

      <div class="score-card" style="border-color: {tierColor}">
        <div class="tier-badge" style="background: {tierColor}">
          {TIER_LABEL[tier]}
        </div>
        <h2>{data.info.Industry}</h2>
        <div class="score-row">
          <span class="score-num" style="color: {tierColor}">
            {(score * 100).toFixed(1)}
          </span>
          <span class="score-label">AI Exposure Score (out of 100)</span>
        </div>
        <p class="tier-desc">
          {#if tier === 'High'}
            Workers in this industry are among the most exposed to AI automation.
            Jobs here involve tasks that AI can perform — such as data analysis,
            writing, and financial processing.
          {:else if tier === 'Medium'}
            This industry has moderate AI exposure. Some tasks are automatable,
            but many still require human judgment and physical presence.
          {:else}
            This industry has low AI exposure. Most work here involves physical
            skills, direct human interaction, or on-site tasks that are difficult
            to automate.
          {/if}
        </p>
      </div>

      <div class="charts">
        <TrendChart
          title="Average Weekly Wage (2022–2024)"
          industryTrend={data.trend}
          tierTrend={data.tier_trend}
          metric="Average Weekly Wage"
          format="$"
          currentTier={tier}
          colors={TIER_COLOR}
        />
        <TrendChart
          title="Average Employment (2022–2024)"
          industryTrend={data.trend}
          tierTrend={data.tier_trend}
          metric="Average Employment"
          format=""
          currentTier={tier}
          colors={TIER_COLOR}
        />
      </div>
    </section>
  {/if}

  <section class="methodology">
    <h2>Methodology & Data Sources</h2>
    <p>
      This tool combines three datasets to estimate how exposed each Houston industry
      is to artificial intelligence, and how that exposure relates to recent wage and
      employment trends.
    </p>

    <div class="method-grid">
      <div class="method-card">
        <h3>AI Exposure Scores</h3>
        <p>
          Occupation-level AI exposure scores come from
          <a href="https://www.anthropic.com/research/labor-market-impacts" target="_blank">
            Anthropic's Economic Index
          </a>
          (2024). Each score (0–1) reflects how much of a job's tasks can be
          performed or assisted by AI, based on real-world Claude usage patterns
          across 756 occupations.
        </p>
      </div>

      <div class="method-card">
        <h3>Industry–Occupation Crosswalk</h3>
        <p>
          To translate occupation-level scores into industry-level scores, we used the
          <a href="https://www.bls.gov/oes/" target="_blank">
            BLS Occupational Employment Statistics (OES) 2024
          </a>
          national industry-specific data. For each 3-digit NAICS industry, we
          computed a weighted average AI exposure score — weighting each occupation's
          score by its employment share in that industry.
        </p>
      </div>

      <div class="method-card">
        <h3>Houston Employment & Wage Data</h3>
        <p>
          Wage and employment trends come from the
          <a href="https://texaslmi.com/LMIbyCategory/QCEW" target="_blank">
            Texas Labor Market Information QCEW
          </a>
          for the Houston–Pasadena–The Woodlands metropolitan area, covering
          Q1 2022 through Q4 2024. Data is reported at the 3-digit NAICS level
          for private-sector employers.
        </p>
      </div>

      <div class="method-card">
        <h3>Tier Classification</h3>
        <p>
          Industries were divided into three equal tiers (High, Medium, Low) using
          quantile-based binning on their weighted AI exposure scores. Each tier
          contains roughly one-third of all matched industries. The tier averages
          shown in the charts represent the mean wage or employment across all
          industries in that tier for each year.
        </p>
      </div>
    </div>

    <div class="limitations">
      <h3>Limitations</h3>
      <ul>
        <li>
          <strong>OES occupation mix is national, not Houston-specific.</strong>
          AI exposure scores are computed using national industry-occupation
          proportions. Houston's economy — particularly its energy sector — may
          have a different workforce composition than the national average, which
          could affect individual industry scores.
        </li>
        <li>
          <strong>Tier averages weight industries equally.</strong> Each industry
          contributes equally to its tier's average, regardless of size. A large
          industry and a small industry are treated the same in the trend comparisons.
        </li>
      </ul>
    </div>
  </section>
</main>

<style>
  :global(body) {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
    background: #f9f7f4;
    color: #1a1a1a;
  }

  main {
    max-width: 860px;
    margin: 0 auto;
    padding: 2rem 1.5rem 4rem;
  }

  header {
    border-bottom: 2px solid #1a1a1a;
    padding-bottom: 1rem;
    margin-bottom: 2rem;
  }

  h1 {
    font-size: 2rem;
    margin: 0 0 0.5rem;
  }

  .subtitle {
    color: #555;
    margin: 0;
    font-size: 1rem;
    line-height: 1.5;
  }

  .selector {
    margin-bottom: 2rem;
  }

  label {
    display: block;
    font-weight: bold;
    margin-bottom: 0.5rem;
    font-size: 0.95rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  select {
    width: 100%;
    padding: 0.75rem 1rem;
    font-size: 1rem;
    border: 2px solid #1a1a1a;
    background: #fff;
    border-radius: 4px;
    cursor: pointer;
  }

  .score-card {
    border: 3px solid #ccc;
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 2rem;
    background: #fff;
    position: relative;
  }

  .tier-badge {
    display: inline-block;
    color: #fff;
    font-size: 0.8rem;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    padding: 0.3rem 0.8rem;
    border-radius: 999px;
    margin-bottom: 0.75rem;
  }

  h2 {
    margin: 0 0 1rem;
    font-size: 1.5rem;
  }

  .score-row {
    display: flex;
    align-items: baseline;
    gap: 0.75rem;
    margin-bottom: 1rem;
  }

  .score-num {
    font-size: 3rem;
    font-weight: bold;
    line-height: 1;
  }

  .score-label {
    font-size: 0.9rem;
    color: #666;
  }

  .tier-desc {
    margin: 0;
    color: #444;
    line-height: 1.6;
    font-size: 0.95rem;
  }

  .charts {
    display: grid;
    gap: 2rem;
  }

  .methodology {
    margin-top: 4rem;
    padding-top: 2rem;
    border-top: 2px solid #1a1a1a;
  }

  .methodology h2 {
    font-size: 1.25rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin: 0 0 0.75rem;
  }

  .methodology > p {
    color: #555;
    line-height: 1.6;
    margin: 0 0 1.5rem;
  }

  .method-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
  }

  .method-card {
    background: #fff;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 1.25rem;
  }

  .method-card h3 {
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin: 0 0 0.5rem;
    color: #333;
  }

  .method-card p {
    font-size: 0.88rem;
    line-height: 1.6;
    color: #555;
    margin: 0;
  }

  .method-card a {
    color: #1a1a1a;
    font-weight: bold;
  }

  .limitations {
    margin-top: 1.5rem;
    padding: 1.25rem 1.5rem;
    background: #fff8f0;
    border: 1px solid #f4a261;
    border-radius: 8px;
  }

  .limitations h3 {
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin: 0 0 0.75rem;
    color: #333;
  }

  .limitations ul {
    margin: 0;
    padding-left: 1.25rem;
    display: grid;
    gap: 0.5rem;
  }

  .limitations li {
    font-size: 0.88rem;
    line-height: 1.6;
    color: #555;
  }
</style>
