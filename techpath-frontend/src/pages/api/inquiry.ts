import type { APIRoute } from 'astro';

export const POST: APIRoute = async ({ request }) => {
  try {
    const data = await request.json();
    const { name, email, company, service, budget, timeline, description } = data;

    // Validate required fields
    if (!name || !email || !service || !description) {
      return new Response(
        JSON.stringify({
          success: false,
          error: 'Name, email, service, and description are required',
        }),
        { status: 400, headers: { 'Content-Type': 'application/json' } }
      );
    }

    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return new Response(
        JSON.stringify({
          success: false,
          error: 'Invalid email format',
        }),
        { status: 400, headers: { 'Content-Type': 'application/json' } }
      );
    }

    // Forward to FastAPI backend
    const apiBaseUrl = import.meta.env.PUBLIC_API_URL || 'http://localhost:8000';
    const response = await fetch(`${apiBaseUrl}/api/v1/inquiries`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name,
        email,
        company: company || null,
        service,
        budget: budget || null,
        timeline: timeline || null,
        description,
      }),
    });

    if (!response.ok) {
      throw new Error('Failed to submit inquiry');
    }

    const result = await response.json();

    return new Response(
      JSON.stringify({
        success: true,
        message: 'Your inquiry has been submitted. Our team will contact you shortly!',
        data: result,
      }),
      { status: 200, headers: { 'Content-Type': 'application/json' } }
    );
  } catch (error) {
    console.error('Service inquiry error:', error);
    return new Response(
      JSON.stringify({
        success: false,
        error: 'An error occurred. Please try again later.',
      }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
};

