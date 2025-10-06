package com.tdebackend.clinicatde.model;

import jakarta.persistence.*;

@Entity
@Table(name = "usuarios")
public class Usuario {
    @Id
    @GeneratedValue (strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 255)
    private String email;

    @Column(nullable = false, length = 255)
    private String nome;

    @Column(nullable = false, length = 10)
    private TipoUsuario tipo;

    @Column(nullable = false)
    private String senha;

    public Usuario() {}

    public Usuario(Long id, String email, String nome, TipoUsuario tipo, String senha) {
        this.id = id;
        this.email = email;
        this.nome = nome;
        this.tipo = tipo;
        this.senha = senha;
    }

    public Long getId() {
        return id;
    }

    public String getEmail() {
        return email;
    }

    public String getNome() {
        return nome;
    }

    public TipoUsuario getTipo() {
        return tipo;
    }

    public String getSenha() {
        return senha;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public void setTipo(TipoUsuario tipo) {
        this.tipo = tipo;
    }

    public void setSenha(String senha) {
        this.senha = senha;
    }
}
