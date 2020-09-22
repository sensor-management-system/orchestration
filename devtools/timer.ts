export interface ITime {
  readonly startTime: Date,
  readonly endTime: Date | null,
  readonly time: number
  stop (): number
}

export class Time implements ITime {
  private _startTime: Date
  private _endTime: Date | null = null

  constructor () {
    this._startTime = new Date()
  }

  get startTime (): Date {
    return this._startTime
  }

  get endTime (): Date | null {
    return this._endTime
  }

  stop (): number {
    this._endTime = new Date()
    return this.time
  }

  get time (): number {
    if (this.endTime === null) {
      return 0
    }
    return this.endTime.getTime() - this.startTime.getTime()
  }
}

export interface ITimer {
  readonly count: number,
  readonly totalTime: number,
  readonly avgTime: number,
  readonly currentTime: number,
  times: ITime[],
  log (message: string): void
}

class Timer {
  public times: ITime[] = []

  get count (): number {
    return this.times.filter(t => t.endTime !== null).length
  }

  get totalTime (): number {
    return this.times.filter(t => t.endTime !== null).reduce((acc, current) => acc + current.time, 0)
  }

  get avgTime (): number {
    return this.totalTime / this.count
  }

  get currentTime (): number {
    const times = this.times.filter(t => t.endTime !== null)
    if (!times.length) {
      return 0
    }
    return times[times.length - 1].time
  }

  log (message: string): void {
    // eslint-disable-next-line no-console
    console && console.log(message, {
      currentTime: this.currentTime,
      totalTime: this.totalTime,
      count: this.count,
      avgTime: this.avgTime,
      times: this.times
    })
  }
}

interface IInternalTimer {
  [name: string]: ITimer
}

const internalTimer: IInternalTimer = {}

/**
 * starts a timer
 *
 * @example
 * // create the timer
 * const timer = startTimer('methodXY')
 * // stop it and log the result to the console
 * timer().log('timer for methodXY')
 *
 * @param {name} string - a name that should be unique to a group of timers
 * @returns {function} a function to stop the timer which returns the timer itself
 */
export const startTimer = (name: string): (() => Timer) => {
  if (!internalTimer[name]) {
    internalTimer[name] = new Timer()
  }
  const time = new Time()
  internalTimer[name].times.push(time)
  return () => {
    time.stop()
    return internalTimer[name]
  }
}
