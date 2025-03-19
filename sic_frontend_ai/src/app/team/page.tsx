import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Github, Linkedin, Mail } from "lucide-react"

export default function AboutUsPage() {
  const developers = [
    {
      name: "Luis Ramos",
      role: "Backend Developer | NextJs Fullstack",
      avatar: "/placeholder.svg?height=100&width=100",
      bio: "Full-stack developer with 3+ years of experience specializing in React with NextJs, and backend development with Django and NestJs. Passionate about clean code and user experience.",
      github: "https://github.com/Ezzz-lui",
      linkedin: "https://linkedin.com/in/lk-ramos",
      email: "ogn.lui@gmail.com",
    },
    {
      name: "Walter Meléndez",
      role: "Python Developer",
      avatar: "/placeholder.svg?height=100&width=100",
      bio: "Python Data Science and Machine Learning Developer, mainly dedicated to learning and applying new technologies to science research ",
      github: "https://github.com/Walter-D3v",
      linkedin: "https://www.linkedin.com/in/walter-cortez-25536a326/",
      email: "walterc.personal@gmail.com",
    },
    {
      name: "Brisa Alvarenga",
      role: "Python Developer",
      avatar: "/placeholder.svg?height=100&width=100",
      bio: "Python and AI student open to understand and learn everything in the enviroment that leads in the actual times.",
      github: "https://github.com/RainDrop-Pi",
      linkedin: "https://www.linkedin.com/in/brisa-zahory-alvarenga-castillo-9093a5353/",
      email: "brizahory.7@gmail.com",
    },
    {
      name: "Ronald Hernandez",
      role: "Junior developer for digital industry || Backend Developer",
      avatar: "/placeholder.svg?height=100&width=100",
      bio: "A Junior Developer for the Digital Industry or Backend Developer Trainee with experience in Python focuses on developing and maintaining backend systems, optimizing data processing, and integrating APIs for digital applications.",
      github: "https://github.com/RonaldHZzzz",
      linkedin: "https://www.linkedin.com/in/ronald-hernandez-4a3aaa310/",
      email: "ronaldhernandez212121@gmail.com",
    }
  ]

  return (
    <div className="container mx-auto py-12 px-4">
      <div className="text-center mb-16">
        <h1 className="text-4xl font-bold tracking-tight mb-4">Development Our Team</h1>
        <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
          We're part of Samsung Innovation Campus - 2025 Edition.
          We develop this proyect to help people to verify the authenticity of news articles using Python, NextJs and Django.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {developers.map((developer) => (
          <Card key={developer.name} className="flex flex-col h-full bg-gradient-to-br from-white via-gray-100 to-white dark:from-black dark:via-zinc-900 dark:to-black shadow-lg backdrop-blur-sm">
            <CardHeader className="flex flex-row items-center gap-4">
              <Avatar className="h-14 w-14">
                <AvatarImage src={developer.avatar} alt={developer.name} />
                <AvatarFallback>
                  {developer.name
                    .split(" ")
                    .map((n) => n[0])
                    .join("")}
                </AvatarFallback>
              </Avatar>
              <div>
                <CardTitle>{developer.name}</CardTitle>
                <CardDescription>
                  <Badge variant="secondary" className="mt-2">
                    {developer.role}
                  </Badge>
                </CardDescription>
              </div>
            </CardHeader>
            <CardContent className="flex-grow">
              <p className="text-muted-foreground">{developer.bio}</p>
            </CardContent>
            <CardFooter className="flex justify-start gap-2 pt-2">
              <Button variant="outline" size="icon" asChild>
                <a
                  href={developer.github}
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label={`${developer.name}'s GitHub`}
                >
                  <Github className="h-4 w-4" />
                </a>
              </Button>
              <Button variant="outline" size="icon" asChild>
                <a
                  href={developer.linkedin}
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label={`${developer.name}'s LinkedIn`}
                >
                  <Linkedin className="h-4 w-4" />
                </a>
              </Button>
              <Button variant="outline" size="icon" asChild>
                <a href={`mailto:${developer.email}`} aria-label={`Email ${developer.name}`}>
                  <Mail className="h-4 w-4" />
                </a>
              </Button>
            </CardFooter>
          </Card>
        ))}
      </div>
    <div className="text-center mt-8">
      <Button variant="default" asChild>
        <a href="/" aria-label="Go to Home">
        Go to Home
        </a>
      </Button>
    </div>
    </div>
  )
}

