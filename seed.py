from app import create_app, db
from app.models import User, Unidade, Configuracao

app = create_app()

with app.app_context():
    
    # ═══════════════════════════════════════
    # CREATE ADMIN
    # ═══════════════════════════════════════
    admin = User(
        email='admin@cond286.pt',
        nome='Miguel Ângelo Rodrigues',
        funcao='admin'
    )
    admin.set_password('Admin@286')
    db.session.add(admin)

    # ═══════════════════════════════════════
    # CREATE UNITS WITH OWNER ACCOUNTS
    # ═══════════════════════════════════════
    unidades_data = [
        {
            'unidade': {
                'codigo': 'R/C ESQ', 'piso': 'R/C', 'posicao': 'ESQ',
                'nome_proprietario': 'Cláudia Ramos / Ricardo Falcão',
                'telefone': '915008680', 'email': 'claudia@cond286.pt'
            },
            'user': {
                'email': 'claudia@cond286.pt',
                'nome': 'Cláudia Ramos',
                'password': 'RCEsq@286'
            }
        },
        {
            'unidade': {
                'codigo': 'R/C DIR', 'piso': 'R/C', 'posicao': 'DIR',
                'nome_proprietario': 'Sofia Marlene Mar...',
                'telefone': '916445291', 'email': 'sofia@cond286.pt'
            },
            'user': {
                'email': 'sofia@cond286.pt',
                'nome': 'Sofia Marlene',
                'password': 'RCDir@286'
            }
        },
        {
            'unidade': {
                'codigo': 'R/C FRT', 'piso': 'R/C', 'posicao': 'FRT',
                'nome_proprietario': 'Marco Paulo Antunes Mourão',
                'telefone': '913811909', 'email': 'marco@cond286.pt'
            },
            'user': {
                'email': 'marco@cond286.pt',
                'nome': 'Marco Paulo Mourão',
                'password': 'RCFrt@286'
            }
        },
        {
            'unidade': {
                'codigo': '1º ESQ', 'piso': '1º', 'posicao': 'ESQ',
                'nome_proprietario': 'Raquel Fragoso da... / Jorge Manuel Mour...',
                'telefone': '914722833', 'email': 'raquel@cond286.pt'
            },
            'user': {
                'email': 'raquel@cond286.pt',
                'nome': 'Raquel Fragoso',
                'password': '1Esq@286'
            }
        },
        {
            'unidade': {
                'codigo': '1º DIR', 'piso': '1º', 'posicao': 'DIR',
                'nome_proprietario': 'Marco Sérgio Ribe... / Custódio Oliveira',
                'telefone': '917976005', 'email': 'marcos@cond286.pt'
            },
            'user': {
                'email': 'marcos@cond286.pt',
                'nome': 'Marco Sérgio Ribeiro',
                'password': '1Dir@286'
            }
        },
        {
            'unidade': {
                'codigo': '1º FRT', 'piso': '1º', 'posicao': 'FRT',
                'nome_proprietario': 'Susana Isabel Lev... / Manuel Sebastião',
                'telefone': '962591777', 'email': 'susana@cond286.pt'
            },
            'user': {
                'email': 'susana@cond286.pt',
                'nome': 'Susana Isabel',
                'password': '1Frt@286'
            }
        },
        {
            'unidade': {
                'codigo': '2º ESQ', 'piso': '2º', 'posicao': 'ESQ',
                'nome_proprietario': 'Valter José Marq...',
                'telefone': '966340230', 'email': 'valter@cond286.pt'
            },
            'user': {
                'email': 'valter@cond286.pt',
                'nome': 'Valter José',
                'password': '2Esq@286'
            }
        },
        {
            'unidade': {
                'codigo': '2º DIR', 'piso': '2º', 'posicao': 'DIR',
                'nome_proprietario': 'Vanda Cristina Santos Rosa',
                'telefone': '936201915', 'email': 'vanda@cond286.pt'
            },
            'user': {
                'email': 'vanda@cond286.pt',
                'nome': 'Vanda Cristina Santos Rosa',
                'password': '2Dir@286'
            }
        },
        {
            'unidade': {
                'codigo': '2º FRT', 'piso': '2º', 'posicao': 'FRT',
                'nome_proprietario': 'Miguel Ângelo Rodrigues (Administrador)',
                'telefone': '966767688', 'email': 'miguel.rodrigues@cond286.pt'
            },
            'user': {
                'email': 'miguel.rodrigues@cond286.pt',
                'nome': 'Miguel Ângelo Rodrigues',
                'password': '2Frt@286'
            }
        },
        {
            'unidade': {
                'codigo': '3º ESQ', 'piso': '3º', 'posicao': 'ESQ',
                'nome_proprietario': 'Fernando Manuel M...',
                'telefone': '967990757', 'email': 'fernando@cond286.pt'
            },
            'user': {
                'email': 'fernando@cond286.pt',
                'nome': 'Fernando Manuel',
                'password': '3Esq@286'
            }
        },
        {
            'unidade': {
                'codigo': '3º DIR', 'piso': '3º', 'posicao': 'DIR',
                'nome_proprietario': 'Isabel Maria Lamp...',
                'telefone': '916128018', 'email': 'isabel@cond286.pt'
            },
            'user': {
                'email': 'isabel@cond286.pt',
                'nome': 'Isabel Maria Lamp',
                'password': '3Dir@286'
            }
        },
        {
            'unidade': {
                'codigo': '3º FRT', 'piso': '3º', 'posicao': 'FRT',
                'nome_proprietario': 'Ilya Broskov / Tetiana Pylypenko',
                'telefone': '928057393', 'email': 'ilya@cond286.pt'
            },
            'user': {
                'email': 'ilya@cond286.pt',
                'nome': 'Ilya Broskov',
                'password': '3Frt@286'
            }
        },
    ]

    for data in unidades_data:
        # Create unit
        unidade = Unidade(**data['unidade'])
        db.session.add(unidade)
        db.session.flush()  # Get the unit ID before creating user
        
        # Create user linked to this unit
        user_data = data['user']
        user = User(
            email=user_data['email'],
            nome=user_data['nome'],
            funcao='owner',
            unidade_id=unidade.id
        )
        user.set_password(user_data['password'])
        db.session.add(user)

    # ═══════════════════════════════════════
    # CREATE SETTINGS
    # ═══════════════════════════════════════
    settings_data = [
        {'chave': 'ultimo_numero_recibo', 'valor': '895'},
        {'chave': 'taxa_juros', 'valor': '10.0'},
        {'chave': 'multa_incumprimento', 'valor': '0.0'},
        {'chave': 'dias_tolerancia', 'valor': '30'},
        {'chave': 'saldo_inicial_banco', 'valor': '2995.83'},
    ]

    for data in settings_data:
        config = Configuracao(**data)
        db.session.add(config)

    db.session.commit()

    # ═══════════════════════════════════════
    # PRINT SUMMARY
    # ═══════════════════════════════════════
    print("=" * 60)
    print("  BASE DE DADOS CRIADA COM SUCESSO!")
    print("=" * 60)
    print()
    print("  ADMIN:")
    print(f"    Email:    admin@cond286.pt")
    print(f"    Password: Admin@286")
    print()
    print("  CONDÓMINOS (12 frações):")
    print(f"    {'Fração':<10} {'Email':<30} {'Password'}")
    print(f"    {'─'*10} {'─'*30} {'─'*12}")
    for data in unidades_data:
        u = data['user']
        unit_code = data['unidade']['codigo']
        print(f"    {unit_code:<10} {u['email']:<30} {u['password']}")
    print()
    print("=" * 60)