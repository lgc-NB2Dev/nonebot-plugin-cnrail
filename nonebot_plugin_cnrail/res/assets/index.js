function adjustLineHeight() {
  /** @type {NodeListOf<HTMLTableRowElement>} */
  const rows = document.querySelectorAll('.station-table tbody tr')

  for (const row of rows) {
    /** @type {HTMLDivElement | null} */
    const point = row.querySelector('.station-point')
    if (point) {
      point.style.setProperty('--line-height', `${row.offsetHeight - 8}px`)
    }
  }
}

try {
  adjustLineHeight()
} catch (error) {
  console.error(error)
}

const done = document.createElement('div')
done.id = 'done'
document.body.appendChild(done)
