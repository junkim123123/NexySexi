import { groq } from 'next-sanity';

export const homeDeepDiveArticlesQuery = groq`
*[_type == "deepDiveArticle" && featuredOnHome == true]
| order(order asc, _createdAt desc)[0...3]{
  _id,
  title,
  "slug": slug.current,
  status,
  category,
  excerpt,
  heroImage
}
`;