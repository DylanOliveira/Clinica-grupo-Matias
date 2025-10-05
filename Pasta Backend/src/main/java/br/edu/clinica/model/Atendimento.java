package br.edu.clinica.model;

import jakarta.persistence.*;
import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.HashSet;
import java.util.Set;

@Entity
@Table(name="atendimentos")
public class Atendimento {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(optional=false)
    @JoinColumn(name="id_paciente")
    private Paciente paciente;

    @ManyToOne(optional=false)
    @JoinColumn(name="id_usuario")
    private Usuario usuario;

    @Column(name="data_hora")
    private LocalDateTime dataHora;

    @Column(nullable=false)
    private String tipo; 

    private String numeroCarteira;

    @Column(nullable=false)
    private BigDecimal valorTotal;

    @ManyToMany
    @JoinTable(name="atendimento_procedimento",
            joinColumns = @JoinColumn(name="id_atendimento"),
            inverseJoinColumns = @JoinColumn(name="id_procedimento"))
    private Set<Procedimento> procedimentos = new HashSet<>();

}
