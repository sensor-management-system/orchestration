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
  count: number,
  totalTime: number,
  avgTime: number,
  times: ITime[]
}

interface IInternalTimer {
  [name: string]: ITimer
}

const timer: IInternalTimer = {}

export const startTimer = (name: string) => {
  if (!timer[name]) {
    timer[name] = {
      count: 0,
      totalTime: 0,
      avgTime: 0,
      times: []
    }
  }
  timer[name].count++
  timer[name].times.push(new Time())
}

export const endTimer = (name: string): ITimer => {
  if (!timer[name]) {
    throw new Error('timer with name ' + name + ' does not exist')
  }
  const theTimer = timer[name]
  const time = theTimer.times[theTimer.times.length - 1].stop()
  theTimer.totalTime += time
  theTimer.avgTime = theTimer.totalTime / theTimer.times.length
  return theTimer
}
