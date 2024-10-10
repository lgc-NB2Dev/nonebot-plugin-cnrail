import { getPalette } from '@monet-color/palette'
import { DEFAULT_VIEWING_CONDITIONS, createColorScheme } from '@monet-color/theme'

function adjustLineHeight() {
  const trElements = document.querySelectorAll<HTMLTableRowElement>(
    '.station-table tbody tr',
  )
  for (const trElem of trElements) {
    const lineHeight = trElem.offsetHeight
    const pointElem = trElem.querySelector<HTMLDivElement>('.station-point')
    pointElem?.style.setProperty('--line-height', `${lineHeight - 8}px`)
  }
}

async function changeThemeColor() {
  const bgUrl = '/bg'

  const resp = await fetch(bgUrl)
  const blob = await resp.blob()
  const dataUrl = URL.createObjectURL(blob)

  const imgElem = document.createElement('img')
  imgElem.src = dataUrl
  await new Promise((resolve, reject) => {
    imgElem.addEventListener('load', resolve)
    imgElem.addEventListener('error', reject)
  })

  const colors = getPalette(imgElem, DEFAULT_VIEWING_CONDITIONS)
  const scheme = createColorScheme(colors[0])

  const cssWillAppend =
    `.bg-wrapper { background-image: url('${dataUrl}'); }\n` +
    `* {` +
    ` --top-bg-color: ${scheme.accent1.get(400)}aa;` +
    ` --top-title-color: ${scheme.accent2.get(50)};` +
    ` --station-table-head-bg-color: ${scheme.accent1.get(100)}aa;` +
    ` --station-table-arrived-line-color: ${scheme.accent1.get(300)};` +
    ` --station-table-head-color: ${scheme.accent1.get(400)};` +
    ` }`

  const styleElem = document.createElement('style')
  styleElem.innerHTML = cssWillAppend
  document.head.appendChild(styleElem)
}

;(async () => {
  adjustLineHeight()
  await changeThemeColor()

  // notify playwright that the page is done
  const doneDivElem = document.createElement('div')
  doneDivElem.id = 'done'
  document.body.appendChild(doneDivElem)
})()
