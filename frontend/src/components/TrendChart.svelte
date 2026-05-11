<script>
  import { onMount, onDestroy } from 'svelte'
  import { Chart, LineController, LineElement, PointElement, LinearScale, CategoryScale, Tooltip, Legend } from 'chart.js'

  Chart.register(LineController, LineElement, PointElement, LinearScale, CategoryScale, Tooltip, Legend)

  export let title = ''
  export let industryTrend = []
  export let tierTrend = []
  export let metric = ''
  export let format = ''
  export let currentTier = ''
  export let colors = {}

  let canvas
  let chart

  const YEARS = [2022, 2023, 2024, 2025]

  function buildDatasets() {
    const industryValues = YEARS.map(y => {
      const row = industryTrend.find(r => r.Year === y)
      return row ? Math.round(row[metric]) : null
    })

    const datasets = [
      {
        label: 'This Industry',
        data: industryValues,
        borderColor: colors[currentTier] || '#333',
        backgroundColor: colors[currentTier] || '#333',
        borderWidth: 3,
        pointRadius: 5,
        tension: 0.3,
      },
    ]

    for (const tier of ['High', 'Medium', 'Low']) {
      if (tier === currentTier) continue
      const values = YEARS.map(y => {
        const row = tierTrend.find(r => r.AI_Tier === tier && r.Year === y)
        return row ? Math.round(row[metric]) : null
      })
      datasets.push({
        label: `${tier} Exposure Avg`,
        data: values,
        borderColor: colors[tier],
        backgroundColor: colors[tier],
        borderWidth: 1.5,
        borderDash: [5, 4],
        pointRadius: 3,
        tension: 0.3,
      })
    }

    return datasets
  }

  onMount(() => {
    chart = new Chart(canvas, {
      type: 'line',
      data: {
        labels: YEARS,
        datasets: buildDatasets(),
      },
      options: {
        responsive: true,
        animation: false,
        plugins: {
          legend: { position: 'bottom' },
          tooltip: {
            callbacks: {
              label: ctx => {
                const val = ctx.parsed.y?.toLocaleString()
                return ` ${ctx.dataset.label}: ${format}${val}`
              },
            },
          },
        },
        scales: {
          y: {
            ticks: {
              callback: val => `${format}${val.toLocaleString()}`,
            },
          },
        },
      },
    })
  })

  onDestroy(() => chart?.destroy())

  $: if (chart && industryTrend.length) {
    chart.data.datasets = buildDatasets()
    chart.update('none')
  }
</script>

<div class="chart-wrap">
  <h3>{title}</h3>
  <canvas bind:this={canvas}></canvas>
</div>

<style>
  .chart-wrap {
    background: #fff;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 1.25rem 1.5rem;
  }

  h3 {
    margin: 0 0 1rem;
    font-size: 1rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #555;
  }
</style>
