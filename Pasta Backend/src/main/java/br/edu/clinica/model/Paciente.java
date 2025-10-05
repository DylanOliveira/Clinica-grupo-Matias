package br.edu.clinica.model;

import jakarta.persistence.*;
import java.time.LocalDate;

@Entity
@Table(name="pacientes")
public class Paciente {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable=false, unique=true)
    private String cpf;

    @Column(nullable=false)
    private String nome;

    @Column(nullable=false, unique=true)
    private String email;

    @Column(nullable=false)
    private String telefone;

    @Column(name="data_nasc")
    private LocalDate dataNasc;

    private String estado;
    private String cidade;
    private String bairro;
    private String cep;
    private String rua;
    private String numero;

    
    private String cpfRespon;
    private String nomeRespon;
    private LocalDate dataNascRespon;
    private String emailRespon;
    private String telefoneRespon;

}
