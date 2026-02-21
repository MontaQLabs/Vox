import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatDate(date: Date): string {
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }).format(date)
}

export function generateVoxId(username?: string): string {
  if (username) {
    return `vox_${username}`
  }
  const randomBytes = Math.random().toString(36).substring(2, 10)
  return `vox_${randomBytes}`
}
