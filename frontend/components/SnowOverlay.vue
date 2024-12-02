<!--
SPDX-FileCopyrightText: 2024
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->

<template>
  <canvas v-if="isWinter" ref="snowCanvas" />
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'
import { currentAsDateTimeObject } from '@/utils/dateHelper'

interface Snowflake {
  x: number
  y: number
  radius: number
  speed: number
  drift: number
  oscillation: number
}

@Component
export default class SnowOverlay extends Vue {
  private width: number = window.innerWidth
  private height: number = window.innerHeight
  private flakeCount: number = 150
  private snowflakes: Snowflake[] = []

  get canvas (): HTMLCanvasElement | undefined {
    return this.$refs.snowCanvas as HTMLCanvasElement | undefined
  }

  mounted () {
    if (!this.isWinter()) { return }

    this.createSnowflakes()
    this.animateSnow()
    this.handleResize()

    window.addEventListener('resize', this.handleResize)
  }

  createSnowflakes () {
    for (let i = 0; i < this.flakeCount; i++) {
      this.snowflakes.push({
        x: Math.random() * this.width,
        y: Math.random() * this.height,
        radius: Math.random() * 3 + 1,
        speed: Math.random() + 0.5,
        drift: Math.random() * 0.5 - 0.25,
        oscillation: Math.random() * 2 * Math.PI
      })
    }
  }

  drawSnowflakes () {
    const ctx = this.canvas?.getContext('2d') ?? null
    if (!ctx) { return }

    ctx.clearRect(0, 0, this.width, this.height)
    ctx.fillStyle = 'white'
    ctx.beginPath()
    this.snowflakes.forEach((flake) => {
      ctx.moveTo(flake.x, flake.y)
      ctx.arc(flake.x, flake.y, flake.radius, 0, Math.PI * 2)
    })
    ctx.fill()
  }

  moveSnowflakes () {
    this.snowflakes.forEach((flake) => {
      flake.y += flake.speed
      flake.x += flake.drift
      flake.x += Math.sin(flake.oscillation) * 0.5
      flake.oscillation += 0.05

      if (flake.y > this.height) {
        flake.y = 0
        flake.x = Math.random() * this.width
      }
      if (flake.x > this.width) {
        flake.x = 0
      } else if (flake.x < 0) {
        flake.x = this.width
      }
    })
  }

  animateSnow () {
    this.drawSnowflakes()
    this.moveSnowflakes()
    requestAnimationFrame(this.animateSnow)
  }

  handleResize () {
    this.width = window.innerWidth
    this.height = window.innerHeight
    if (!this.canvas) { return }
    this.canvas.width = this.width
    this.canvas.height = this.height
  }

  isWinter (): boolean {
    return [12, 1, 2].includes(currentAsDateTimeObject().month)
  }
}
</script>

<style scoped>
canvas {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 9999;
}
</style>
