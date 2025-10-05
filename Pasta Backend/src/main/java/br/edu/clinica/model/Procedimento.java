package br.edu.clinica.model;

import jakarta.persistence.*;
import java.math.BigDecimal;

@Entity
@Table(name="procedimentos")
public class Procedimento {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable=false, unique=true)
    private String nome;

    @Column(nullable=false, columnDefinition="TEXT")
    private String descricao;

    @Column(nullable=false)
    private BigDecimal valorPlano;

    @Column(nullable=false)
    private BigDecimal valorParticular;

    
}
