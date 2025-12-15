import { defineCollection, z } from 'astro:content';

/**
 * Blog Collection
 * Articles, tutorials, and updates
 */
const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    author: z.string(),
    image: z.string().optional(),
    tags: z.array(z.string()).default([]),
    readingTime: z.number().optional(),
    draft: z.boolean().default(false),
  }),
});

/**
 * Services Collection
 * Service offerings and details
 */
const services = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    icon: z.string(),
    features: z.array(z.string()),
    price: z.string().optional(),
    cta: z.string(),
    order: z.number().default(0),
  }),
});

export const collections = {
  blog,
  services,
};

