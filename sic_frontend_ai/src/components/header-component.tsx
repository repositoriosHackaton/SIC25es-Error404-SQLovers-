'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet'
import { Card, CardContent } from '@/components/ui/card'
import { Menu } from 'lucide-react'
import { ThemeToggle } from '@/components/theme-toggle'

const navItems = [
  { href: '#projects', label: 'Projects' },
  { href: '#experience', label: 'Experience' },
]

export function Header() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <Card className="sticky border-hidden top-4 z-50 mx-4 mt-4 bg-gradient-to-r from-white via-gray-100 to-white dark:from-black dark:via-zinc-900 dark:to-black shadow-lg backdrop-blur-sm">
      <CardContent className="p-0">
        <div className="container mx-auto px-4 py-2">
          <div className="flex justify-between items-center">
            <div className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-neutral-600 to-zinc-600 dark:from-neutral-200 dark:via-zinc-400 dark:to-zinc-200">
            </div>
            <nav className="hidden md:flex items-center space-x-6">
              {navItems.map((item) => (
                <a
                  key={item.href}
                  href={item.href}
                  className="font-semibold text-gray-700 dark:text-gray-300 hover:text-zinc-600 dark:hover:text-zinc-400 transition duration-300"
                >
                  {item.label}
                </a>
              ))}
              <ThemeToggle />
            </nav>
            <div className="flex items-center md:hidden">
              <ThemeToggle />
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}