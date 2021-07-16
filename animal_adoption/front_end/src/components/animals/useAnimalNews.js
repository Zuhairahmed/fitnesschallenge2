import { useState } from 'react'

export default function useAnimalNews(url) {
  const [news, setNews] = useState([])

  async function fetchAnimalNews() {
    try {
      const { message } = await fetch(url ?? '/get-recent-news-items').then((res) => res.json())
      if (message) {
        setNews(message)
      }
    } catch (e) {
      console.error(e)
    }
  }

  return {
    news,
    setNews,
    fetchAnimalNews,
  }
}
