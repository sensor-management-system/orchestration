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
    console.log(message, {
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

export const startTimer = (name: string) => {
  if (!internalTimer[name]) {
    internalTimer[name] = new Timer()
  }
  internalTimer[name].times.push(new Time())
}

export const endTimer = (name: string): ITimer => {
  if (!internalTimer[name]) {
    throw new Error('timer with name ' + name + ' does not exist')
  }
  const timer = internalTimer[name]
  timer.times[timer.times.length - 1].stop()
  return timer
}
