function Dashboard({ stats }) {
  const cards = [
    { label: 'Total Tasks', value: stats.total },
    { label: 'Completed', value: stats.completed },
    { label: 'Pending', value: stats.pending },
    { label: 'High Priority', value: stats.highPriority },
  ];

  return (
    <section className="dashboard" aria-label="Task summary dashboard">
      {cards.map((card) => (
        <article className="dashboard-card" key={card.label}>
          <span>{card.label}</span>
          <strong>{card.value}</strong>
        </article>
      ))}
    </section>
  );
}

export default Dashboard;
