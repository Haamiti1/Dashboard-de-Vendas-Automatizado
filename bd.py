from sqlachemy import create_engine, Table, Column, Integer, Float, MetaData

engine = create_engine("postgresql://usuario:senha@host:porta/nome_do_banco")
conn = engine.connect()

metadata = MetaData()
tabela_dashboard = Table("dashboard_vendas", metadata,
    Column("id", Integer, primary_key=True),
    Column("total_vendas", Float),
    Column("total_pedidos", Integer),
    Column("total_clientes", Integer)
)

metadata.create_all(engine)

conn.execute(
    tabela_dashboard.insert().values(
        total_vendas=total_vendas,
        total_pedidos=total_pedidos,
        total_clientes=total_clientes
    )
)