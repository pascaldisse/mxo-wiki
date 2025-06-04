# Code Generation Templates for MXO Development
**Automating the Liberation Through Smart Templates**

> *"The Matrix is a system, Neo. That system is our enemy."* - Morpheus (But we can turn its patterns into our templates.)

## 🎯 **The Power of Code Generation**

Why write the same code patterns repeatedly when we can teach machines to generate them? This guide provides battle-tested templates for automatically generating Matrix Online server components, client modifications, and tool development - turning hours of work into seconds of generation.

## 🏗️ **Template Architecture**

### Core Template System

```python
# template_engine.py
import jinja2
import yaml
import os
from datetime import datetime
from pathlib import Path

class MXOTemplateEngine:
    def __init__(self, template_dir='templates'):
        self.template_dir = Path(template_dir)
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.template_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Add custom filters
        self.env.filters['camelcase'] = self.camelcase
        self.env.filters['snakecase'] = self.snakecase
        self.env.filters['pascalcase'] = self.pascalcase
        
        # Add global variables
        self.env.globals['now'] = datetime.now
        self.env.globals['year'] = datetime.now().year
        
    def render_template(self, template_name, context):
        """Render a template with given context"""
        template = self.env.get_template(template_name)
        return template.render(**context)
        
    def generate_from_spec(self, spec_file, output_dir):
        """Generate code from specification file"""
        with open(spec_file, 'r') as f:
            spec = yaml.safe_load(f)
            
        results = []
        for item in spec['generate']:
            template_name = item['template']
            output_file = Path(output_dir) / item['output']
            context = item.get('context', {})
            
            # Merge global context
            context.update(spec.get('global_context', {}))
            
            # Generate code
            code = self.render_template(template_name, context)
            
            # Create output directory if needed
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file
            with open(output_file, 'w') as f:
                f.write(code)
                
            results.append({
                'template': template_name,
                'output': str(output_file),
                'success': True
            })
            
        return results
        
    @staticmethod
    def camelcase(text):
        """Convert to camelCase"""
        parts = text.split('_')
        return parts[0].lower() + ''.join(p.capitalize() for p in parts[1:])
        
    @staticmethod
    def snakecase(text):
        """Convert to snake_case"""
        import re
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
        
    @staticmethod
    def pascalcase(text):
        """Convert to PascalCase"""
        return ''.join(word.capitalize() for word in text.split('_'))
```

## 📦 **Packet Handler Templates**

### Base Packet Handler Template

```csharp
// templates/packet_handler.cs.j2
using System;
using System.IO;
using MXOServer.Core;
using MXOServer.Network;
using MXOServer.Database;

namespace MXOServer.Handlers
{
    /// <summary>
    /// Handles {{ packet_name }} packets (0x{{ opcode|format_hex }})
    /// {{ description }}
    /// </summary>
    public class {{ handler_name }}Handler : IPacketHandler
    {
        private readonly ILogger _logger;
        private readonly IDatabase _database;
        {% if requires_auth %}
        private readonly IAuthService _authService;
        {% endif %}
        
        public byte Opcode => 0x{{ opcode|format_hex }};
        public string Name => "{{ packet_name }}";
        
        public {{ handler_name }}Handler(
            ILogger logger,
            IDatabase database{% if requires_auth %},
            IAuthService authService{% endif %}
        )
        {
            _logger = logger;
            _database = database;
            {% if requires_auth %}_authService = authService;{% endif %}
        }
        
        public async Task HandleAsync(IClient client, IPacket packet)
        {
            _logger.Debug($"Handling {{ packet_name }} from {client.Id}");
            
            try
            {
                // Parse packet data
                var data = Parse{{ packet_name }}(packet);
                
                {% if requires_auth %}
                // Verify authentication
                if (!await _authService.IsAuthenticatedAsync(client))
                {
                    await SendErrorResponseAsync(client, ErrorCode.NotAuthenticated);
                    return;
                }
                {% endif %}
                
                // Validate data
                var validation = await ValidateAsync(client, data);
                if (!validation.IsValid)
                {
                    await SendErrorResponseAsync(client, validation.ErrorCode);
                    return;
                }
                
                // Process request
                var result = await ProcessAsync(client, data);
                
                // Send response
                await SendResponseAsync(client, result);
                
                _logger.Info($"{{ packet_name }} handled successfully for {client.Id}");
            }
            catch (Exception ex)
            {
                _logger.Error($"Error handling {{ packet_name }}: {ex.Message}", ex);
                await SendErrorResponseAsync(client, ErrorCode.InternalError);
            }
        }
        
        private {{ packet_name }}Data Parse{{ packet_name }}(IPacket packet)
        {
            using var reader = new BinaryReader(packet.GetStream());
            
            return new {{ packet_name }}Data
            {
                {% for field in fields %}
                {{ field.name|pascalcase }} = reader.Read{{ field.read_type }}(),
                {% endfor %}
            };
        }
        
        private async Task<ValidationResult> ValidateAsync(IClient client, {{ packet_name }}Data data)
        {
            {% for validation in validations %}
            // {{ validation.description }}
            if ({{ validation.condition }})
            {
                return ValidationResult.Invalid(ErrorCode.{{ validation.error_code }});
            }
            
            {% endfor %}
            return ValidationResult.Valid();
        }
        
        private async Task<{{ packet_name }}Result> ProcessAsync(IClient client, {{ packet_name }}Data data)
        {
            // TODO: Implement business logic
            {% if has_database %}
            
            // Database operations
            await using var transaction = await _database.BeginTransactionAsync();
            try
            {
                // Perform database operations
                
                await transaction.CommitAsync();
            }
            catch
            {
                await transaction.RollbackAsync();
                throw;
            }
            {% endif %}
            
            return new {{ packet_name }}Result
            {
                Success = true,
                // TODO: Set result data
            };
        }
        
        private async Task SendResponseAsync(IClient client, {{ packet_name }}Result result)
        {
            var response = new Packet(0x{{ response_opcode|format_hex }});
            using var writer = new BinaryWriter(response.GetStream());
            
            {% for field in response_fields %}
            writer.Write(result.{{ field.name|pascalcase }});
            {% endfor %}
            
            await client.SendAsync(response);
        }
        
        private async Task SendErrorResponseAsync(IClient client, ErrorCode errorCode)
        {
            var response = new Packet(0x{{ error_opcode|format_hex }});
            using var writer = new BinaryWriter(response.GetStream());
            
            writer.Write((ushort)errorCode);
            writer.Write(errorCode.GetDescription());
            
            await client.SendAsync(response);
        }
    }
    
    public class {{ packet_name }}Data
    {
        {% for field in fields %}
        public {{ field.type }} {{ field.name|pascalcase }} { get; set; }
        {% endfor %}
    }
    
    public class {{ packet_name }}Result
    {
        public bool Success { get; set; }
        {% for field in response_fields %}
        public {{ field.type }} {{ field.name|pascalcase }} { get; set; }
        {% endfor %}
    }
}
```

### Packet Handler Specification

```yaml
# specs/login_handler.yaml
global_context:
  namespace: MXOServer.Handlers.Authentication
  author: Liberation Developer

generate:
  - template: packet_handler.cs.j2
    output: Handlers/Authentication/LoginHandler.cs
    context:
      packet_name: Login
      handler_name: Login
      opcode: 0x01
      response_opcode: 0x02
      error_opcode: 0xFF
      description: Handles player login requests
      requires_auth: false
      has_database: true
      
      fields:
        - name: username
          type: string
          read_type: String
        - name: password_hash
          type: byte[]
          read_type: Bytes(32)
        - name: client_version
          type: int
          read_type: Int32
          
      validations:
        - description: Check username length
          condition: data.Username.Length < 3 || data.Username.Length > 20
          error_code: InvalidUsername
        - description: Check client version
          condition: data.ClientVersion < MIN_CLIENT_VERSION
          error_code: OutdatedClient
          
      response_fields:
        - name: session_token
          type: byte[]
        - name: character_count
          type: int
        - name: server_time
          type: long
```

## 🎮 **Ability System Templates**

### Ability Class Template

```csharp
// templates/ability.cs.j2
using System;
using System.Threading.Tasks;
using MXOServer.Core;
using MXOServer.Combat;
using MXOServer.Entities;

namespace MXOServer.Abilities.{{ category|pascalcase }}
{
    /// <summary>
    /// {{ ability_name }} - {{ description }}
    /// </summary>
    [Ability(
        Id = {{ ability_id }},
        Name = "{{ ability_name }}",
        Category = AbilityCategory.{{ category }},
        TargetType = TargetType.{{ target_type }}
    )]
    public class {{ class_name }} : AbilityBase
    {
        // Ability parameters
        {% for param in parameters %}
        private const {{ param.type }} {{ param.name|upper }} = {{ param.value }};
        {% endfor %}
        
        public override async Task<bool> CanUseAsync(ICharacter caster, ITarget target)
        {
            // Base checks
            if (!await base.CanUseAsync(caster, target))
                return false;
                
            {% for requirement in requirements %}
            // {{ requirement.description }}
            if ({{ requirement.check }})
            {
                await caster.SendSystemMessageAsync("{{ requirement.message }}");
                return false;
            }
            
            {% endfor %}
            return true;
        }
        
        public override async Task<AbilityResult> ExecuteAsync(ICharacter caster, ITarget target)
        {
            var result = new AbilityResult();
            
            try
            {
                // Start ability animation
                await caster.PlayAnimationAsync(AnimationId.{{ animation }});
                
                {% if cast_time > 0 %}
                // Cast time
                var castResult = await caster.CastAsync(this, {{ cast_time }});
                if (!castResult.Success)
                {
                    result.Success = false;
                    result.Reason = castResult.InterruptReason;
                    return result;
                }
                {% endif %}
                
                // Apply effects
                {% for effect in effects %}
                await Apply{{ effect.type }}Async(caster, target, result);
                {% endfor %}
                
                // Consume resources
                {% if inner_strength_cost > 0 %}
                caster.ConsumeInnerStrength({{ inner_strength_cost }});
                {% endif %}
                
                // Set cooldown
                {% if cooldown > 0 %}
                caster.SetAbilityCooldown(Id, TimeSpan.FromSeconds({{ cooldown }}));
                {% endif %}
                
                // Success
                result.Success = true;
                
                // Broadcast ability use
                await BroadcastAbilityUseAsync(caster, target);
                
                // Log for analytics
                LogAbilityUse(caster, target, result);
                
            }
            catch (Exception ex)
            {
                Logger.Error($"Error executing {{ ability_name }}: {ex.Message}", ex);
                result.Success = false;
                result.Reason = "An error occurred";
            }
            
            return result;
        }
        
        {% for effect in effects %}
        private async Task Apply{{ effect.type }}Async(ICharacter caster, ITarget target, AbilityResult result)
        {
            {% if effect.type == "Damage" %}
            var damage = CalculateDamage(caster, target, {{ effect.base_damage }}, DamageType.{{ effect.damage_type }});
            
            if (target is ICharacter targetChar)
            {
                var actualDamage = await targetChar.TakeDamageAsync(damage, caster);
                result.DamageDealt = actualDamage;
                
                // Check for additional effects
                {% if effect.has_dot %}
                await targetChar.AddEffectAsync(new DamageOverTimeEffect(
                    caster,
                    {{ effect.dot_damage }},
                    TimeSpan.FromSeconds({{ effect.dot_duration }}),
                    TimeSpan.FromSeconds({{ effect.dot_interval }})
                ));
                {% endif %}
            }
            {% elif effect.type == "Heal" %}
            if (target is ICharacter targetChar)
            {
                var healAmount = CalculateHealing(caster, {{ effect.base_heal }});
                var actualHeal = await targetChar.HealAsync(healAmount, caster);
                result.HealingDone = actualHeal;
            }
            {% elif effect.type == "Buff" %}
            if (target is ICharacter targetChar)
            {
                var buff = new {{ effect.buff_type }}Buff(
                    caster,
                    {{ effect.buff_value }},
                    TimeSpan.FromSeconds({{ effect.buff_duration }})
                );
                await targetChar.AddEffectAsync(buff);
                result.BuffsApplied.Add(buff.Name);
            }
            {% elif effect.type == "Debuff" %}
            if (target is ICharacter targetChar && !targetChar.IsImmuneTo(DebuffType.{{ effect.debuff_type }}))
            {
                var debuff = new {{ effect.debuff_type }}Debuff(
                    caster,
                    {{ effect.debuff_value }},
                    TimeSpan.FromSeconds({{ effect.debuff_duration }})
                );
                await targetChar.AddEffectAsync(debuff);
                result.DebuffsApplied.Add(debuff.Name);
            }
            {% endif %}
        }
        {% endfor %}
        
        protected override void ConfigureVisuals()
        {
            // Visual effects configuration
            VisualEffects = new VisualEffectConfig
            {
                {% if visual_effects.cast %}
                CastEffect = new VisualEffect
                {
                    Id = VisualEffectId.{{ visual_effects.cast }},
                    AttachPoint = AttachPoint.Hands,
                    Duration = {{ cast_time }}f
                },
                {% endif %}
                {% if visual_effects.impact %}
                ImpactEffect = new VisualEffect
                {
                    Id = VisualEffectId.{{ visual_effects.impact }},
                    AttachPoint = AttachPoint.Target,
                    Duration = 2.0f
                },
                {% endif %}
                {% if visual_effects.projectile %}
                ProjectileEffect = new VisualEffect
                {
                    Id = VisualEffectId.{{ visual_effects.projectile }},
                    Speed = {{ visual_effects.projectile_speed }}f
                }
                {% endif %}
            };
            
            // Sound configuration
            SoundEffects = new SoundEffectConfig
            {
                {% for sound in sound_effects %}
                {{ sound.event|pascalcase }} = SoundId.{{ sound.id }},
                {% endfor %}
            };
        }
    }
}
```

### Ability Specification Example

```yaml
# specs/abilities/viral_abilities.yaml
global_context:
  category: Viral
  author: Liberation Developer

generate:
  - template: ability.cs.j2
    output: Abilities/Viral/CodePulse.cs
    context:
      ability_name: Code Pulse
      class_name: CodePulseAbility
      ability_id: 0x200
      description: Unleashes a pulse of viral code that damages all nearby enemies
      target_type: Self
      animation: CodePulse
      
      parameters:
        - name: base_damage
          type: float
          value: 150.0
        - name: radius
          type: float
          value: 10.0
        - name: max_targets
          type: int
          value: 6
          
      requirements:
        - description: Check if in combat
          check: "!caster.IsInCombat"
          message: "You must be in combat to use Code Pulse"
        - description: Check inner strength
          check: "caster.InnerStrength < 50"
          message: "Not enough Inner Strength"
          
      cast_time: 1.5
      inner_strength_cost: 50
      cooldown: 30
      
      effects:
        - type: Damage
          base_damage: BASE_DAMAGE
          damage_type: Viral
          has_dot: true
          dot_damage: 25
          dot_duration: 6
          dot_interval: 2
          
      visual_effects:
        cast: ViralCastGreen
        impact: ViralExplosion
        
      sound_effects:
        - event: cast_start
          id: Viral_Cast_01
        - event: impact
          id: Viral_Explosion_01
```

## 🗄️ **Database Model Templates**

### Entity Model Template

```csharp
// templates/entity_model.cs.j2
using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using MXOServer.Database.Core;

namespace MXOServer.Database.Models
{
    /// <summary>
    /// {{ entity_description }}
    /// </summary>
    [Table("{{ table_name }}")]
    public class {{ entity_name }} : EntityBase
    {
        {% for property in properties %}
        {% if property.description %}
        /// <summary>
        /// {{ property.description }}
        /// </summary>
        {% endif %}
        {% for attribute in property.attributes %}
        [{{ attribute }}]
        {% endfor %}
        public {{ property.type }}{% if property.nullable %}?{% endif %} {{ property.name }} { get; set; }{% if property.default %} = {{ property.default }};{% endif %}
        
        {% endfor %}
        
        #region Navigation Properties
        {% for navigation in navigations %}
        
        public virtual {{ navigation.type }} {{ navigation.name }} { get; set; }
        {% endfor %}
        
        #endregion
        
        #region Computed Properties
        {% for computed in computed_properties %}
        
        [NotMapped]
        public {{ computed.type }} {{ computed.name }}
        {
            get
            {
                {{ computed.getter|indent(16) }}
            }
        }
        {% endfor %}
        
        #endregion
        
        #region Methods
        
        public override void OnBeforeSave()
        {
            base.OnBeforeSave();
            {% for property in properties %}
            {% if property.before_save %}
            
            // {{ property.before_save.description }}
            {{ property.before_save.code|indent(12) }}
            {% endif %}
            {% endfor %}
        }
        
        {% for method in methods %}
        public {{ method.return_type }} {{ method.name }}({{ method.parameters }})
        {
            {{ method.body|indent(12) }}
        }
        
        {% endfor %}
        #endregion
    }
}
```

### Repository Template

```csharp
// templates/repository.cs.j2
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using MXOServer.Database.Core;
using MXOServer.Database.Models;

namespace MXOServer.Database.Repositories
{
    public interface I{{ entity_name }}Repository : IRepository<{{ entity_name }}>
    {
        {% for method in interface_methods %}
        Task<{{ method.return_type }}> {{ method.name }}Async({{ method.parameters }});
        {% endfor %}
    }
    
    public class {{ entity_name }}Repository : RepositoryBase<{{ entity_name }}>, I{{ entity_name }}Repository
    {
        public {{ entity_name }}Repository(MXODbContext context) : base(context)
        {
        }
        
        {% for method in repository_methods %}
        public async Task<{{ method.return_type }}> {{ method.name }}Async({{ method.parameters }})
        {
            {% if method.include_related %}
            var query = DbSet
                {% for include in method.includes %}
                .Include(x => x.{{ include }})
                {% endfor %}
                .AsQueryable();
            {% else %}
            var query = DbSet.AsQueryable();
            {% endif %}
            
            {% for where in method.where_clauses %}
            query = query.Where(x => {{ where }});
            {% endfor %}
            
            {% if method.order_by %}
            query = query.OrderBy(x => x.{{ method.order_by }});
            {% elif method.order_by_desc %}
            query = query.OrderByDescending(x => x.{{ method.order_by_desc }});
            {% endif %}
            
            {% if method.take %}
            query = query.Take({{ method.take }});
            {% endif %}
            
            {% if method.skip %}
            query = query.Skip({{ method.skip }});
            {% endif %}
            
            {% if method.return_single %}
            return await query.FirstOrDefaultAsync();
            {% elif method.return_count %}
            return await query.CountAsync();
            {% elif method.return_exists %}
            return await query.AnyAsync();
            {% else %}
            return await query.ToListAsync();
            {% endif %}
        }
        
        {% endfor %}
        
        protected override IQueryable<{{ entity_name }}> GetIncludes(IQueryable<{{ entity_name }}> query)
        {
            return query
                {% for include in default_includes %}
                .Include(x => x.{{ include }})
                {% endfor %};
        }
    }
}
```

## 🌐 **API Endpoint Templates**

### Controller Template

```csharp
// templates/api_controller.cs.j2
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using MXOServer.API.Core;
using MXOServer.Services;
using MXOServer.Models;

namespace MXOServer.API.Controllers
{
    /// <summary>
    /// {{ controller_description }}
    /// </summary>
    [ApiController]
    [Route("api/[controller]")]
    {% if requires_auth %}[Authorize]{% endif %}
    public class {{ controller_name }}Controller : ApiControllerBase
    {
        private readonly I{{ service_name }}Service _service;
        private readonly ILogger<{{ controller_name }}Controller> _logger;
        
        public {{ controller_name }}Controller(
            I{{ service_name }}Service service,
            ILogger<{{ controller_name }}Controller> logger)
        {
            _service = service;
            _logger = logger;
        }
        
        {% for endpoint in endpoints %}
        /// <summary>
        /// {{ endpoint.description }}
        /// </summary>
        {% for param in endpoint.parameters %}
        /// <param name="{{ param.name }}">{{ param.description }}</param>
        {% endfor %}
        /// <returns>{{ endpoint.returns }}</returns>
        [Http{{ endpoint.method|capitalize }}{% if endpoint.route %}("{{ endpoint.route }}"){% endif %}]
        {% if endpoint.authorize %}[Authorize({{ endpoint.authorize }})]{% endif %}
        {% if endpoint.produces %}[Produces("{{ endpoint.produces }}")]{% endif %}
        public async Task<ActionResult<{{ endpoint.return_type }}>> {{ endpoint.name }}Async(
            {% for param in endpoint.parameters %}
            {% if param.from_route %}[FromRoute]{% elif param.from_query %}[FromQuery]{% elif param.from_body %}[FromBody]{% endif %} {{ param.type }} {{ param.name }}{% if not loop.last %},{% endif %}
            {% endfor %}
        )
        {
            try
            {
                {% if endpoint.validate_model %}
                if (!ModelState.IsValid)
                {
                    return BadRequest(ModelState);
                }
                {% endif %}
                
                {% for validation in endpoint.validations %}
                // {{ validation.description }}
                if ({{ validation.condition }})
                {
                    return BadRequest(new ErrorResponse
                    {
                        Message = "{{ validation.message }}",
                        Code = "{{ validation.code }}"
                    });
                }
                
                {% endfor %}
                
                // Call service
                var result = await _service.{{ endpoint.service_method }}Async(
                    {% for param in endpoint.service_params %}
                    {{ param }}{% if not loop.last %},{% endif %}
                    {% endfor %}
                );
                
                {% if endpoint.check_null %}
                if (result == null)
                {
                    return NotFound(new ErrorResponse
                    {
                        Message = "{{ endpoint.not_found_message }}",
                        Code = "NOT_FOUND"
                    });
                }
                {% endif %}
                
                {% if endpoint.transform_result %}
                // Transform result
                var response = {{ endpoint.transform_result }};
                return Ok(response);
                {% else %}
                return Ok(result);
                {% endif %}
            }
            catch ({{ endpoint.catch_exception|default('Exception') }} ex)
            {
                _logger.LogError(ex, "Error in {{ endpoint.name }}");
                {% if endpoint.catch_exception %}
                return StatusCode(500, new ErrorResponse
                {
                    Message = ex.Message,
                    Code = "{{ endpoint.error_code }}"
                });
                {% else %}
                return StatusCode(500, new ErrorResponse
                {
                    Message = "An error occurred",
                    Code = "INTERNAL_ERROR"
                });
                {% endif %}
            }
        }
        
        {% endfor %}
    }
}
```

## 🧪 **Test Generation Templates**

### Unit Test Template

```csharp
// templates/unit_test.cs.j2
using System;
using System.Threading.Tasks;
using Xunit;
using Moq;
using FluentAssertions;
using MXOServer.{{ namespace }};

namespace MXOServer.Tests.{{ namespace }}
{
    public class {{ test_class_name }}Tests
    {
        private readonly Mock<I{{ dependency1 }}> _{{ dependency1|camelcase }}Mock;
        {% for dep in additional_dependencies %}
        private readonly Mock<I{{ dep }}> _{{ dep|camelcase }}Mock;
        {% endfor %}
        private readonly {{ class_under_test }} _sut;
        
        public {{ test_class_name }}Tests()
        {
            _{{ dependency1|camelcase }}Mock = new Mock<I{{ dependency1 }}>();
            {% for dep in additional_dependencies %}
            _{{ dep|camelcase }}Mock = new Mock<I{{ dep }}>();
            {% endfor %}
            
            _sut = new {{ class_under_test }}(
                _{{ dependency1|camelcase }}Mock.Object{% for dep in additional_dependencies %},
                _{{ dep|camelcase }}Mock.Object{% endfor %}
            );
        }
        
        {% for test in test_cases %}
        [Fact]
        public async Task {{ test.method }}_{{ test.scenario }}_{{ test.expected_behavior }}()
        {
            // Arrange
            {% for arrange in test.arrange %}
            {{ arrange }};
            {% endfor %}
            
            // Act
            {% if test.is_async %}
            var result = await _sut.{{ test.method }}Async({{ test.parameters }});
            {% else %}
            var result = _sut.{{ test.method }}({{ test.parameters }});
            {% endif %}
            
            // Assert
            {% for assertion in test.assertions %}
            {{ assertion }};
            {% endfor %}
            
            {% if test.verify_mocks %}
            // Verify
            {% for verify in test.verifications %}
            {{ verify }};
            {% endfor %}
            {% endif %}
        }
        
        {% endfor %}
        
        #region Helper Methods
        
        {% for helper in helper_methods %}
        private {{ helper.return_type }} {{ helper.name }}({{ helper.parameters }})
        {
            {{ helper.body|indent(12) }}
        }
        
        {% endfor %}
        
        #endregion
    }
}
```

### Integration Test Template

```csharp
// templates/integration_test.cs.j2
using System;
using System.Net;
using System.Net.Http;
using System.Threading.Tasks;
using Xunit;
using FluentAssertions;
using Microsoft.AspNetCore.Mvc.Testing;
using MXOServer.Tests.Fixtures;

namespace MXOServer.Tests.Integration
{
    [Collection("Integration")]
    public class {{ test_class_name }}IntegrationTests : IClassFixture<WebApplicationFactory<Startup>>
    {
        private readonly WebApplicationFactory<Startup> _factory;
        private readonly HttpClient _client;
        
        public {{ test_class_name }}IntegrationTests(WebApplicationFactory<Startup> factory)
        {
            _factory = factory;
            _client = _factory
                .WithWebHostBuilder(builder =>
                {
                    builder.ConfigureServices(services =>
                    {
                        // Override services for testing
                    });
                })
                .CreateClient();
        }
        
        {% for test in integration_tests %}
        [Fact]
        public async Task {{ test.name }}_ReturnsExpectedResult()
        {
            // Arrange
            {% if test.auth_required %}
            _client.DefaultRequestHeaders.Authorization = 
                new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", TestTokens.ValidToken);
            {% endif %}
            
            {% if test.request_body %}
            var request = new {{ test.request_type }}
            {
                {% for prop in test.request_properties %}
                {{ prop.name }} = {{ prop.value }},
                {% endfor %}
            };
            var content = new StringContent(
                JsonSerializer.Serialize(request),
                Encoding.UTF8,
                "application/json"
            );
            {% endif %}
            
            // Act
            var response = await _client.{{ test.http_method }}Async(
                "{{ test.endpoint }}"{% if test.request_body %},
                content{% endif %}
            );
            
            // Assert
            response.StatusCode.Should().Be(HttpStatusCode.{{ test.expected_status }});
            
            {% if test.response_assertions %}
            var responseContent = await response.Content.ReadAsStringAsync();
            var result = JsonSerializer.Deserialize<{{ test.response_type }}>(responseContent);
            
            {% for assertion in test.response_assertions %}
            result.{{ assertion.property }}.Should().{{ assertion.matcher }}({{ assertion.expected }});
            {% endfor %}
            {% endif %}
        }
        
        {% endfor %}
    }
}
```

## 🛠️ **Tool Generation Templates**

### CLI Tool Template

```python
# templates/cli_tool.py.j2
#!/usr/bin/env python3
"""
{{ tool_name }} - {{ tool_description }}
Generated for The Matrix Online Liberation Project
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('{{ tool_name|snakecase }}')


class {{ tool_name|pascalcase }}:
    """Main class for {{ tool_name }}"""
    
    def __init__(self, config: dict = None):
        self.config = config or {}
        {% for attribute in attributes %}
        self.{{ attribute.name }} = {{ attribute.default }}
        {% endfor %}
        
    {% for command in commands %}
    def {{ command.name }}(self, {% for param in command.params %}{{ param.name }}: {{ param.type }}{% if param.default %} = {{ param.default }}{% endif %}{% if not loop.last %}, {% endif %}{% endfor %}) -> {{ command.return_type }}:
        """
        {{ command.description }}
        
        Args:
            {% for param in command.params %}
            {{ param.name }}: {{ param.description }}
            {% endfor %}
            
        Returns:
            {{ command.return_description }}
        """
        logger.info(f"Executing {{ command.name }} command")
        
        try:
            {% for validation in command.validations %}
            # {{ validation.description }}
            if {{ validation.condition }}:
                raise ValueError("{{ validation.error }}")
                
            {% endfor %}
            
            # Implementation
            {{ command.implementation|indent(12) }}
            
        except Exception as e:
            logger.error(f"Error in {{ command.name }}: {e}")
            raise
            
    {% endfor %}


def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        description='{{ tool_description }}',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
{% for example in examples %}
  {{ example }}
{% endfor %}

For more information, visit the MXO Liberation Wiki
        """
    )
    
    # Global options
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '-c', '--config',
        type=Path,
        help='Configuration file path'
    )
    
    # Add subcommands
    subparsers = parser.add_subparsers(
        dest='command',
        help='Available commands'
    )
    
    {% for command in commands %}
    # {{ command.name }} command
    {{ command.name }}_parser = subparsers.add_parser(
        '{{ command.name|kebabcase }}',
        help='{{ command.description }}'
    )
    {% for arg in command.cli_args %}
    {{ command.name }}_parser.add_argument(
        '{{ arg.flags }}',
        {% if arg.type %}type={{ arg.type }},{% endif %}
        {% if arg.default %}default={{ arg.default }},{% endif %}
        {% if arg.required %}required=True,{% endif %}
        {% if arg.action %}action='{{ arg.action }}',{% endif %}
        help='{{ arg.help }}'
    )
    {% endfor %}
    
    {% endfor %}
    
    return parser


def main():
    """Main entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        
    # Load configuration
    config = {}
    if args.config and args.config.exists():
        import json
        with open(args.config) as f:
            config = json.load(f)
            
    # Create tool instance
    tool = {{ tool_name|pascalcase }}(config)
    
    # Execute command
    if not args.command:
        parser.print_help()
        return 1
        
    try:
        command_method = getattr(tool, args.command.replace('-', '_'))
        # Convert args to dict and filter for command params
        kwargs = {k: v for k, v in vars(args).items() 
                 if k not in ['command', 'verbose', 'config']}
        result = command_method(**kwargs)
        
        # Handle result
        if result:
            print(result)
            
        return 0
        
    except Exception as e:
        logger.error(f"Command failed: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
```

## 🎮 **Game Content Templates**

### Mission Template

```xml
<!-- templates/mission.xml.j2 -->
<?xml version="1.0" encoding="UTF-8"?>
<Mission>
    <Header>
        <Id>{{ mission_id }}</Id>
        <Name>{{ mission_name }}</Name>
        <Description>{{ description }}</Description>
        <Level>{{ level }}</Level>
        <Type>{{ mission_type }}</Type>
        <Repeatable>{{ repeatable|lower }}</Repeatable>
        <Faction>{{ faction|default('Neutral') }}</Faction>
    </Header>
    
    <Requirements>
        {% for req in requirements %}
        <Requirement type="{{ req.type }}">
            {% if req.type == 'Level' %}
            <MinLevel>{{ req.min_level }}</MinLevel>
            {% elif req.type == 'Mission' %}
            <MissionId>{{ req.mission_id }}</MissionId>
            <Status>{{ req.status|default('Completed') }}</Status>
            {% elif req.type == 'Item' %}
            <ItemId>{{ req.item_id }}</ItemId>
            <Quantity>{{ req.quantity|default(1) }}</Quantity>
            {% elif req.type == 'Reputation' %}
            <Faction>{{ req.faction }}</Faction>
            <MinReputation>{{ req.min_reputation }}</MinReputation>
            {% endif %}
        </Requirement>
        {% endfor %}
    </Requirements>
    
    <Objectives>
        {% for objective in objectives %}
        <Objective id="{{ loop.index }}">
            <Type>{{ objective.type }}</Type>
            <Description>{{ objective.description }}</Description>
            {% if objective.type == 'Kill' %}
            <Target>
                <NPCType>{{ objective.npc_type }}</NPCType>
                <Quantity>{{ objective.quantity }}</Quantity>
                {% if objective.location %}
                <Location>{{ objective.location }}</Location>
                {% endif %}
            </Target>
            {% elif objective.type == 'Collect' %}
            <Item>
                <ItemId>{{ objective.item_id }}</ItemId>
                <Quantity>{{ objective.quantity }}</Quantity>
                {% if objective.drop_chance %}
                <DropChance>{{ objective.drop_chance }}</DropChance>
                {% endif %}
            </Item>
            {% elif objective.type == 'Interact' %}
            <InteractionTarget>
                <ObjectId>{{ objective.object_id }}</ObjectId>
                {% if objective.interaction_time %}
                <InteractionTime>{{ objective.interaction_time }}</InteractionTime>
                {% endif %}
            </InteractionTarget>
            {% elif objective.type == 'Escort' %}
            <EscortTarget>
                <NPCId>{{ objective.npc_id }}</NPCId>
                <StartLocation>{{ objective.start_location }}</StartLocation>
                <EndLocation>{{ objective.end_location }}</EndLocation>
            </EscortTarget>
            {% endif %}
            {% if objective.optional %}
            <Optional>true</Optional>
            {% endif %}
        </Objective>
        {% endfor %}
    </Objectives>
    
    <Rewards>
        <Experience>{{ rewards.experience }}</Experience>
        <Information>{{ rewards.information }}</Information>
        {% if rewards.money %}
        <Money>{{ rewards.money }}</Money>
        {% endif %}
        {% if rewards.items %}
        <Items>
            {% for item in rewards.items %}
            <Item id="{{ item.id }}" quantity="{{ item.quantity|default(1) }}"{% if item.chance %} chance="{{ item.chance }}"{% endif %} />
            {% endfor %}
        </Items>
        {% endif %}
        {% if rewards.reputation %}
        <Reputation>
            {% for rep in rewards.reputation %}
            <Change faction="{{ rep.faction }}" amount="{{ rep.amount }}" />
            {% endfor %}
        </Reputation>
        {% endif %}
        {% if rewards.abilities %}
        <Abilities>
            {% for ability in rewards.abilities %}
            <Ability id="{{ ability }}" />
            {% endfor %}
        </Abilities>
        {% endif %}
    </Rewards>
    
    <Dialogue>
        {% for dialogue in dialogues %}
        <Entry id="{{ dialogue.id }}" speaker="{{ dialogue.speaker }}">
            <Trigger>{{ dialogue.trigger }}</Trigger>
            <Text>{{ dialogue.text }}</Text>
            {% if dialogue.choices %}
            <Choices>
                {% for choice in dialogue.choices %}
                <Choice>
                    <Text>{{ choice.text }}</Text>
                    <Next>{{ choice.next }}</Next>
                    {% if choice.condition %}
                    <Condition>{{ choice.condition }}</Condition>
                    {% endif %}
                </Choice>
                {% endfor %}
            </Choices>
            {% endif %}
        </Entry>
        {% endfor %}
    </Dialogue>
    
    <Scripts>
        {% if scripts.on_accept %}
        <OnAccept>
            <![CDATA[
            {{ scripts.on_accept|indent(12) }}
            ]]>
        </OnAccept>
        {% endif %}
        {% if scripts.on_complete %}
        <OnComplete>
            <![CDATA[
            {{ scripts.on_complete|indent(12) }}
            ]]>
        </OnComplete>
        {% endif %}
        {% if scripts.on_abandon %}
        <OnAbandon>
            <![CDATA[
            {{ scripts.on_abandon|indent(12) }}
            ]]>
        </OnAbandon>
        {% endif %}
    </Scripts>
</Mission>
```

## 🔧 **Template Usage Examples**

### Generate Multiple Packet Handlers

```python
# generate_handlers.py
from pathlib import Path
import yaml

# Define all packet handlers
handlers = [
    {
        'name': 'Movement',
        'opcode': 0x10,
        'fields': [
            {'name': 'x', 'type': 'float', 'read_type': 'Single'},
            {'name': 'y', 'type': 'float', 'read_type': 'Single'},
            {'name': 'z', 'type': 'float', 'read_type': 'Single'},
            {'name': 'rotation', 'type': 'float', 'read_type': 'Single'}
        ]
    },
    {
        'name': 'Combat',
        'opcode': 0x20,
        'fields': [
            {'name': 'ability_id', 'type': 'int', 'read_type': 'Int32'},
            {'name': 'target_id', 'type': 'int', 'read_type': 'Int32'}
        ]
    },
    # ... more handlers
]

# Generate specifications
for handler in handlers:
    spec = {
        'global_context': {
            'namespace': 'MXOServer.Handlers',
            'author': 'Generated'
        },
        'generate': [{
            'template': 'packet_handler.cs.j2',
            'output': f'Handlers/{handler["name"]}Handler.cs',
            'context': {
                'packet_name': handler['name'],
                'handler_name': handler['name'],
                'opcode': handler['opcode'],
                'fields': handler['fields'],
                # ... more context
            }
        }]
    }
    
    # Save specification
    with open(f'specs/{handler["name"].lower()}_handler.yaml', 'w') as f:
        yaml.dump(spec, f)
```

### Batch Generate Abilities

```python
# generate_abilities.py
ability_categories = {
    'Martial Arts': {
        'abilities': [
            {
                'name': 'Hyper Kick',
                'id': 0x100,
                'damage': 120,
                'animation': 'MartialArtsKick'
            },
            {
                'name': 'Speed Punch',
                'id': 0x101,
                'damage': 80,
                'animation': 'MartialArtsPunch'
            }
        ]
    },
    'Hacker': {
        'abilities': [
            {
                'name': 'Logic Bomb',
                'id': 0x200,
                'damage': 150,
                'animation': 'HackerCast'
            }
        ]
    }
}

for category, data in ability_categories.items():
    for ability in data['abilities']:
        # Generate ability specification
        # Run template engine
        pass
```

## 🎨 **Custom Template Creation**

### Creating Your Own Templates

```python
# custom_template_guide.py
"""
Guide for creating custom templates for MXO development
"""

# 1. Define template structure
template_structure = """
{# Template Header #}
// Generated by {{ generator_name }}
// Date: {{ now().strftime('%Y-%m-%d') }}
// Purpose: {{ purpose }}

{# Imports Section #}
{% for import in imports %}
{{ import }}
{% endfor %}

{# Main Content #}
namespace {{ namespace }}
{
    public class {{ class_name }}
    {
        {# Use loops for repetitive structures #}
        {% for property in properties %}
        public {{ property.type }} {{ property.name }} { get; set; }
        {% endfor %}
        
        {# Conditional sections #}
        {% if has_constructor %}
        public {{ class_name }}({{ constructor_params }})
        {
            // Constructor implementation
        }
        {% endif %}
        
        {# Include other templates #}
        {% include 'partials/methods.j2' %}
    }
}
"""

# 2. Create template helpers
def create_template_helpers():
    return {
        'format_hex': lambda x: f"{x:02X}",
        'pluralize': lambda word: word + 's' if not word.endswith('s') else word,
        'indent': lambda text, spaces: '\n'.join(' ' * spaces + line for line in text.split('\n')),
        'kebabcase': lambda text: text.lower().replace('_', '-').replace(' ', '-'),
    }

# 3. Validation function
def validate_template_context(context, required_fields):
    """Ensure all required fields are present"""
    missing = [field for field in required_fields if field not in context]
    if missing:
        raise ValueError(f"Missing required fields: {missing}")
```

## Remember

> *"There is no spoon."* - Neo

There are no limits to what you can generate. These templates are not rigid rules but flexible patterns that bend to your will. Every line of generated code is a step toward liberation, every template a tool for freedom.

The Matrix Online's resurrection doesn't require writing every line by hand - it requires understanding patterns and teaching machines to replicate them. With these templates, you hold the power to generate entire systems with a single command.

**Define the pattern. Generate the code. Free the Matrix.**

---

**Template Status**: 🟢 PRODUCTION READY  
**Generation Power**: ⚡ MAXIMUM  
**Liberation Factor**: 🔥🔥🔥🔥🔥  

*In patterns we trust. In generation we scale. In templates we liberate.*

---

[← Development Hub](index.md) | [→ AI Mission Writing](ai-mission-writing.md) | [→ Server Architecture](../02-server-setup/server-architecture.md)